from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.weather_service import get_weather, get_planting_recommendation
from utils.ai_service import detect_disease, get_roboflow_raw_prediction, identify_crop
from utils.disease_guide import CROP_NAME_MAP, DISEASE_GUIDE
import logging
logger = logging.getLogger(__name__)
analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route('/crops', methods=['GET'])
def get_supported_crops():
    crop_diseases = {}
    for disease_key, disease_info in DISEASE_GUIDE.items():
        crop_name = disease_info.get('crop_name', 'Unknown')
        if crop_name not in crop_diseases:
            crop_diseases[crop_name] = []
        crop_diseases[crop_name].append({'disease': disease_key, 'description': disease_info.get('description', '')})
    return (jsonify({'supported_crops': sorted(list(crop_diseases.keys())), 'crops_and_diseases': crop_diseases}), 200)

@analyze_bp.route('/debug/test-disease', methods=['POST'])
def debug_test_disease():
    try:
        file = request.files.get('file')
        expected_crop = request.form.get('crop')
        if not file:
            return (jsonify({'error': 'Image file is required'}), 400)
        raw_response = get_roboflow_raw_prediction(file)
        logger.info(f'DEBUG: Raw Roboflow response: {raw_response}')
        file.seek(0)
        disease_result = detect_disease(file, expected_crop=expected_crop, return_all=True)
        return (jsonify({'raw_roboflow_response': raw_response, 'processed_result': disease_result}), 200)
    except Exception as e:
        logger.error(f'Debug Error: {str(e)}', exc_info=True)
        return (jsonify({'error': f'Debug error: {str(e)}'}), 500)

@analyze_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    try:
        file = request.files.get('file')
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        user_crop = request.form.get('crop')
        
        if not file:
            return (jsonify({'error': 'Image file is required'}), 400)
        if not lat or not lon:
            return (jsonify({'error': 'Latitude and Longitude are required'}), 400)
        if not user_crop:
            supported_crops = list(set([info.get('crop_name') for info in DISEASE_GUIDE.values()]))
            return (jsonify({'error': 'Crop type is required', 'info': 'Please specify which crop you are analyzing', 'supported_crops': sorted(supported_crops), 'example_crops': ['Maize', 'Tomato', 'Bean', 'Potato']}), 400)
        
        crop_key = user_crop.lower().strip()
        crop_info = CROP_NAME_MAP.get(crop_key)
        if not crop_info:
            supported_crops = sorted(list(set([v['name'] for v in CROP_NAME_MAP.values()])))
            return (jsonify({'error': f"Crop '{user_crop}' not recognized", 'supported_crops': supported_crops}), 400)
        
        current_user = get_jwt_identity()
        weather_result = get_weather(lat, lon)
        if not weather_result['success']:
            return (jsonify({'error': weather_result['error']}), 500)

        disease_result = detect_disease(file, expected_crop=crop_key, require_crop_match=True)
        if not disease_result['success']:
            return (jsonify({'error': disease_result['error'], 'expected_crop': crop_key, 'crop_info': crop_info}), 400)
        
        temp = weather_result.get('temperature_celsius')
        recommendation = get_planting_recommendation(temp)
        disease_info = disease_result['disease_info']
        
        recommendations = []
        if isinstance(temp, (int, float)):
            recommendations.append(f'Current temperature is {temp}°C. {recommendation}.')
        else:
            recommendations.append(f'{recommendation}.')
        
        if disease_result.get('disease_name') and disease_result.get('disease_name').lower() not in ['healthy_crop', 'unknown disease']:
            recommendations.append(f"Detected disease: {disease_result.get('disease_name')}.")
            if disease_info.get('prevention'):
                recommendations.append('Prevention: ' + '; '.join(disease_info.get('prevention', [])))
            if disease_info.get('control'):
                recommendations.append('Control: ' + '; '.join(disease_info.get('control', [])))
        else:
            recommendations.append(f'{crop_info["name"]} appears healthy. Continue good farming practices and monitor regularly.')
        
        if disease_result.get('warning'):
            recommendations.append(f"Note: {disease_result.get('warning')}")
        
        recommendation_summary = '\n'.join(recommendations)
        result = {
            'success': True,
            'user': current_user,
            'location': f'{lat},{lon}',
            'crop_specified': crop_info['name'],
            'crop_scientific_name': crop_info['scientific'],
            'recommendation': recommendation,
            'recommendation_summary': recommendation_summary,
            'recommendations': recommendations,
            'weather': weather_result.get('description'),
            'temperature_celsius': temp,
            'diseaseName': disease_result['disease_name'],
            'diseaseConfidence': disease_result.get('confidence', 0),
            'diseaseDescription': disease_info.get('description', 'No description available'),
            'prevention': disease_info.get('prevention', []),
            'control': disease_info.get('control', []),
            'details': disease_result['disease_details'],
            'all_predictions': disease_result.get('all_predictions', [])
        }
        logger.info(f"Analysis complete for user {current_user}: Crop={crop_info['name']}, Disease={disease_result['disease_name']}, Confidence={disease_result.get('confidence')}")
        return (jsonify(result), 200)
    except Exception as e:
        logger.error(f'Analyze Error: {str(e)}', exc_info=True)
        return (jsonify({'error': f'Server error: {str(e)}'}), 500)