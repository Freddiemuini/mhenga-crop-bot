from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.weather_service import get_weather, get_planting_recommendation
from utils.ai_service import detect_disease, get_roboflow_raw_prediction
import logging

logger = logging.getLogger(__name__)

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/debug/test-disease', methods=['POST'])
def debug_test_disease():
    """Debug endpoint to test disease detection without authentication.

    Accepts an optional `crop` form field to exercise the expected_crop logic.
    """
    try:
        file = request.files.get("file")
        expected_crop = request.form.get("crop")
        if not file:
            return jsonify({"error": "Image file is required"}), 400

        raw_response = get_roboflow_raw_prediction(file)
        logger.info(f"DEBUG: Raw Roboflow response: {raw_response}")
        
        file.seek(0)
        disease_result = detect_disease(file, expected_crop=expected_crop, return_all=True)
        
        return jsonify({
            "raw_roboflow_response": raw_response,
            "processed_result": disease_result
        }), 200
    except Exception as e:
        logger.error(f"Debug Error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Debug error: {str(e)}"}), 500


@analyze_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    try:
        file = request.files.get("file")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        user_crop = request.form.get("crop")  # optional expected crop from user

        if not file:
            return jsonify({"error": "Image file is required"}), 400
        if not lat or not lon:
            return jsonify({"error": "Latitude and Longitude are required"}), 400

        current_user = get_jwt_identity()

        weather_result = get_weather(lat, lon)
        if not weather_result["success"]:
            return jsonify({"error": weather_result["error"]}), 500

        disease_result = detect_disease(file, expected_crop=user_crop)
        if not disease_result["success"]:
            return jsonify({"error": disease_result["error"]}), 500

        temp = weather_result.get("temperature_celsius")
        recommendation = get_planting_recommendation(temp)

        disease_info = disease_result["disease_info"]
        
        result = {
            "user": current_user,
            "location": f"{lat},{lon}",
            "recommendation": recommendation,
            "weather": weather_result.get("description"),
            "temperature_celsius": temp,
            "diseaseName": disease_result["disease_name"],
            "diseaseConfidence": disease_result.get("confidence", 0),
            "diseaseDescription": disease_info.get("description", "No description available"),
            "prevention": disease_info.get("prevention", []),
            "control": disease_info.get("control", []),
            "details": disease_result["disease_details"],
            "cropEnglishName": disease_info.get("crop_name", "Unknown Crop"),
            "cropScientificName": disease_info.get("crop_scientific_name", "Unknown"),
            "all_predictions": disease_result.get("all_predictions", [])
        }
        # include user-supplied crop for debugging
        if user_crop:
            result["userCrop"] = user_crop

        logger.info(f"Analysis complete for user {current_user}: Disease={disease_result['disease_name']}, Crop={disease_info.get('crop_name')}, Scientific Name={disease_info.get('crop_scientific_name')}")
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Analyze Error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Server error: {str(e)}"}), 500
