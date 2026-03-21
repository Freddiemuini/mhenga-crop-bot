import io
import pytest
import requests
from utils import ai_service

class DummyResponse:

    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(response=self)

def make_image():
    return io.BytesIO(b'dummy')

def test_detect_disease_return_all(monkeypatch):
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.8}, {'class': 'maize_rust', 'confidence': 0.5}]}

    def fake_post(*args, **kwargs):
        return DummyResponse(fake)
    monkeypatch.setattr(requests, 'post', fake_post)
    result = ai_service.detect_disease(make_image(), return_all=True)
    assert result['success']
    assert 'all_predictions' in result
    assert len(result['all_predictions']) == 2
    assert result['raw'] == fake

def test_detect_disease_expected_crop_filters(monkeypatch):
    fake = {'predictions': [{'class': 'tomato_early_blight', 'confidence': 0.8}, {'class': 'maize_rust', 'confidence': 0.7}]}
    monkeypatch.setattr(requests, 'post', lambda *a, **k: DummyResponse(fake))
    result = ai_service.detect_disease(make_image(), expected_crop='maize')
    assert result['success']
    assert result['disease_name'] == 'maize_rust'
    assert result['confidence'] == 0.7
    assert any((p['crop_matches'] for p in result.get('all_predictions', [])))