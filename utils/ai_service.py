import requests
import logging
from config import ROBOFLOW_API_KEY, ROBOFLOW_MODEL_ID, ROBOFLOW_MODEL_VERSION
from utils.disease_guide import get_disease_info, CROP_NAME_MAP, DISEASE_GUIDE

logger = logging.getLogger(__name__)


def validate_prediction(disease_name, confidence):
    """Validate if prediction makes sense and is trustworthy
    
    Returns:
        (is_valid, confidence_level, reason)
    """
    if confidence < 0.3:
        return False, confidence, "Confidence too low (< 30%)"
    
    # Check if the disease name is in our database
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
    """Get raw Roboflow prediction without processing"""
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
    """Get all predictions from Roboflow, not just the first one"""
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


def detect_disease(image_file, min_confidence=0.5):
    """Detect disease using Roboflow AI model
    
    Args:
        image_file: The image file to analyze
        min_confidence: Minimum confidence threshold (0-1). Defaults to 0.5 (50%)
    """
    try:
        image_file.seek(0)  # Reset file pointer
        response = requests.post(
            f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}/{ROBOFLOW_MODEL_VERSION}",
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": image_file.read()},
            timeout=30
        )
        response.raise_for_status()
        rf_result = response.json()

        logger.info(f"Roboflow API Response: {rf_result}")

        if "predictions" in rf_result and len(rf_result["predictions"]) > 0:
            # Try each prediction until we find a valid one
            for idx, prediction in enumerate(rf_result["predictions"][:3]):  # Try top 3
                disease_name = prediction.get("class", "Unknown Disease")
                confidence = prediction.get("confidence", 0)
                
                logger.info(f"Prediction {idx+1}: '{disease_name}' with confidence: {confidence:.2%}")
                
                # Validate this prediction
                is_valid, conf, reason = validate_prediction(disease_name, confidence)
                logger.info(f"Validation result: {reason}")
                
                if is_valid:
                    # Use this prediction
                    disease_details = str(prediction)
                    disease_info = get_disease_info(disease_name)
                    
                    logger.info(f"Using prediction: {disease_name} -> Crop: {disease_info.get('crop_name')}")
                    
                    return {
                        "success": True,
                        "disease_name": disease_name,
                        "confidence": confidence,
                        "disease_info": disease_info,
                        "disease_details": disease_details
                    }
            
            # If no valid predictions found, use first one but flag it
            prediction = rf_result["predictions"][0]
            disease_name = prediction.get("class", "Unknown Disease")
            confidence = prediction.get("confidence", 0)
            disease_details = str(prediction)
            
            logger.warning(f"No valid predictions found. Using unvalidated: {disease_name}")
            
            disease_info = get_disease_info(disease_name)
            
            return {
                "success": True,
                "disease_name": disease_name,
                "confidence": confidence,
                "disease_info": disease_info,
                "disease_details": disease_details,
                "warning": "Prediction may not be accurate. Please consult a local agricultural officer."
            }
            
        else:
            disease_name = "Unknown Disease"
            confidence = 0
            disease_details = "No predictions from model."
            disease_info = {
                "crop_name": "Unable to Identify",
                "crop_scientific_name": "Unknown",
                "description": "Could not identify any crop/disease. Please provide a clearer image showing the affected plant part or consult a local agricultural extension officer.",
                "prevention": ["General good farming practices"],
                "control": ["Consult local agricultural extension officer for identification and treatment"]
            }
            logger.warning("No predictions returned from Roboflow model")

            return {
                "success": True,
                "disease_name": disease_name,
                "confidence": confidence,
                "disease_info": disease_info,
                "disease_details": disease_details
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
