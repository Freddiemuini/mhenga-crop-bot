import requests
import logging
from config import ROBOFLOW_API_KEY, ROBOFLOW_MODEL_ID, ROBOFLOW_MODEL_VERSION
from utils.disease_guide import get_disease_info, CROP_NAME_MAP, DISEASE_GUIDE

logger = logging.getLogger(__name__)


def validate_prediction(disease_name, confidence):
    if confidence < 0.3:
        return False, confidence, "Confidence too low (< 30%)"
    
    disease_key = disease_name.lower().replace(" ", "_").replace("-", "_")
    
    is_in_db = False
    for key in DISEASE_GUIDE.keys():
        if disease_key == key or disease_key in DISEASE_GUIDE[key].get("aliases", []):
            is_in_db = True
            break
    
    if is_in_db and confidence >= 0.6:
        return True, confidence, "Valid - in database with good confidence"
    elif is_in_db and confidence >= 0.4:
        return True, confidence, "Valid - in database but lower confidence"
    else:
        return False, confidence, f"Not found in disease database"


def get_roboflow_raw_prediction(image_file):
    try:
        image_file.seek(0)
        response = requests.post(
            f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}",
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": image_file.read()},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Roboflow raw prediction error: {str(e)}", exc_info=True)
        return {"error": str(e)}


def get_all_predictions(image_file):
    try:
        image_file.seek(0)
        response = requests.post(
            f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}",
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": image_file.read()},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting Roboflow predictions: {str(e)}", exc_info=True)
        return None


def detect_disease(image_file, min_confidence=0.5, expected_crop=None, return_all=False):
    try:
        image_file.seek(0)
        response = requests.post(
            f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}",
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": image_file.read()},
            timeout=30
        )
        response.raise_for_status()
        rf_result = response.json()

        logger.info(f"Roboflow API Response: {rf_result}")

        predictions = rf_result.get("predictions", [])
        structured = []
        for pred in predictions:
            name = pred.get("class", "Unknown Disease")
            conf = pred.get("confidence", 0)
            info = get_disease_info(name)
            crop_matches = False
            if expected_crop:
                key = expected_crop.lower().strip()
                crop_matches = key in info.get("crop_name", "").lower() or key in info.get("crop_scientific_name", "").lower()
            structured.append({
                "class": name,
                "confidence": conf,
                "disease_info": info,
                "crop_matches": crop_matches
            })

        if return_all:
            return {
                "success": True,
                "all_predictions": structured,
                "raw": rf_result
            }

        chosen = None
        warning = None
        for pred in sorted(structured, key=lambda x: (not x["crop_matches"], -x["confidence"])):
            name = pred["class"]
            conf = pred["confidence"]
            if conf < min_confidence:
                continue
            is_valid, conf2, reason = validate_prediction(name, conf)
            logger.info(f"Evaluating prediction '{name}' ({conf:.2%}): {reason}")
            if is_valid:
                chosen = pred
                break
        if not chosen and structured:
            chosen = structured[0]
            warning = "Model predictions did not meet validation criteria; using top result."

        if chosen:
            return_val = {
                "success": True,
                "disease_name": chosen["class"],
                "confidence": chosen["confidence"],
                "disease_info": chosen["disease_info"],
                "disease_details": str(chosen)
            }
            if warning:
                return_val["warning"] = warning
            if expected_crop and not chosen.get("crop_matches"):
                return_val["warning"] = return_val.get("warning", "") + (
                    " Prediction does not match expected crop."
                )
            return_val["all_predictions"] = structured
            return return_val
        else:
            logger.warning("No predictions returned from Roboflow model")
            disease_info = {
                "crop_name": "Unable to Identify",
                "crop_scientific_name": "Unknown",
                "description": "Could not identify any crop/disease. Please provide a clearer image showing the affected plant part or consult a local agricultural extension officer.",
                "prevention": ["General good farming practices"],
                "control": ["Consult local agricultural extension officer for identification and treatment"]
            }
            return {
                "success": True,
                "disease_name": "Unknown Disease",
                "confidence": 0,
                "disease_info": disease_info,
                "disease_details": "No predictions from model.",
                "all_predictions": structured
            }

    except requests.exceptions.HTTPError as e:
        logger.error(f"Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}")
        return {
            "success": False,
            "error": f"Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}"
        }
    except Exception as e:
        logger.error(f"Roboflow API failed: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Roboflow API failed: {str(e)}"
        }

    except requests.exceptions.HTTPError as e:
        logger.error(f"Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}")
        return {
            "success": False,
            "error": f"Roboflow API HTTP Error: {e.response.status_code} - {e.response.text}"
        }
    except Exception as e:
        logger.error(f"Roboflow API failed: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Roboflow API failed: {str(e)}"
        }
