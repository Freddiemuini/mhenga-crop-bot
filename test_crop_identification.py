import requests
import os

ROBOFLOW_API_KEY = "ctkt12G5XN3jQUlLIiIk"
ROBOFLOW_CROP_MODEL_ID = "crop-identification-model"
ROBOFLOW_CROP_MODEL_VERSION = "1"

def test_crop_identification(image_path, expected_crop):
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                f"https://detect.roboflow.com/{ROBOFLOW_CROP_MODEL_ID}/{ROBOFLOW_CROP_MODEL_VERSION}",
                params={"api_key": ROBOFLOW_API_KEY},
                files={"file": image_file.read()},
                timeout=30
            )

        response.raise_for_status()
        result = response.json()

        predictions = result.get("predictions", [])
        if not predictions:
            return {"error": "No predictions returned"}

        top_prediction = max(predictions, key=lambda x: x.get("confidence", 0))
        detected_crop = top_prediction.get("class", "").lower().strip()
        confidence = top_prediction.get("confidence", 0)

        correct = detected_crop == expected_crop.lower()

        return {
            "expected_crop": expected_crop,
            "detected_crop": detected_crop,
            "confidence": confidence,
            "correct": correct,
            "all_predictions": predictions
        }
    except Exception as e:
        return {"error": str(e)}

def batch_test_crop_identification(test_images_dir, crop_mapping):
    results = []
    crop_stats = {}

    for filename in os.listdir(test_images_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        image_path = os.path.join(test_images_dir, filename)
        expected_crop = None

        for crop, patterns in crop_mapping.items():
            if any(pattern in filename.lower() for pattern in patterns):
                expected_crop = crop
                break

        if not expected_crop:
            print(f"Skipping {filename}: cannot determine expected crop")
            continue

        if expected_crop not in crop_stats:
            crop_stats[expected_crop] = {"total": 0, "correct": 0}

        crop_stats[expected_crop]["total"] += 1

        result = test_crop_identification(image_path, expected_crop)
        results.append(result)

        if "error" in result:
            print(f"❌ {filename}: Error - {result['error']}")
            continue

        correct = result.get("correct", False)
        detected = result.get("detected_crop", "unknown")
        confidence = result.get("confidence", 0)

        if correct:
            crop_stats[expected_crop]["correct"] += 1
            print(f"✅ {filename}: Correct ({detected}, {confidence:.1%})")
        else:
            print(f"❌ {filename}: Expected: {expected_crop} | Detected: {detected} | Confidence: {confidence:.1%}")

    total_images = len(results)
    correct_predictions = sum(1 for r in results if r.get("correct", False))

    accuracy = correct_predictions / total_images if total_images > 0 else 0
    print(f"\n📊 TEST RESULTS SUMMARY")
    print(f"Total Images: {total_images}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Overall Accuracy: {accuracy:.1%}")

    print("\nPer-Crop Accuracy:")
    for crop, stats in crop_stats.items():
        crop_accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        print(f"{crop}: {crop_accuracy:.1%}")
    return results

if __name__ == "__main__":
    print("Crop Identification Testing Script")
    print("Usage: python test_crop_identification.py")
    print("Make sure to set up test images in a directory and call batch_test_crop_identification")