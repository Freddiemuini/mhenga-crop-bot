# Mhenga Crop Bot

This project is a Flask-based crop disease analysis API powered by Roboflow and weather data.

## ✅ Deploying to Render
Follow these steps to deploy this project on Render.

### 1) Push your repo to a Git host (GitHub/GitLab)
If you haven't already, initialize a git repo and push to a remote:

```bash
# Initialize (if not already initialized)
git init

git add .
git commit -m "Initial commit"

# Add a remote (replace with your repo URL)
git remote add origin https://github.com/<your-username>/<your-repo>.git

git push -u origin main
```

### 2) Sign up / log in to Render
- Go to: https://render.com
- Connect your GitHub/GitLab account.

### 3) Create a new Web Service
- Click **New** → **Web Service**
- Select the repo you pushed.
- Render should detect Python and use `render.yaml` for configuration.

### 4) Set environment variables
In the Render dashboard, go to your service’s **Environment** tab and add the following (recommended values shown as placeholders):

- `AGROMONITORING_API_KEY` = `your_agromonitoring_api_key`
- `ROBOFLOW_API_KEY` = `your_roboflow_api_key`
- `ROBOFLOW_MODEL_ID` = `your_roboflow_model_id`
- `ROBOFLOW_MODEL_VERSION` = `your_roboflow_model_version`
- `JWT_SECRET_KEY` = `some_secret_value`
- `MAIL_SERVER` = `smtp.gmail.com` (or your mail SMTP host)
- `MAIL_PORT` = `587`
- `MAIL_USERNAME` = `your_email@example.com`
- `MAIL_PASSWORD` = `your_email_password_or_app_password`
- `MAIL_SENDER_NAME` = `AgriBot`
- `MAIL_SENDER_EMAIL` = `your_email@example.com`

(Optional) If you want a persistent database rather than local sqlite, set:
- `DATABASE_URL` = `postgres://...` (Render Postgres add-on or external DB)

**Crop Identification (Optional):**
- `ROBOFLOW_CROP_MODEL_ID` = `your_crop_identification_model_id`
- `ROBOFLOW_CROP_MODEL_VERSION` = `1`

### 5) Deploy
Once variables are set, Render will build and deploy your service.

### 6) Verify
After deployment, visit the service URL Render provides and test the `/` endpoint.

---

## 🛠 Local development
Run locally with:

```bash
python app.py
```

Then send requests to `http://127.0.0.0:5000`.

## Features

### Crop Disease Detection
- Upload plant images to detect diseases
- Supports multiple crops: maize, tomato, beans, potato, wheat, rice, etc.
- Provides treatment recommendations and prevention tips

### Automatic Crop Identification (NEW)
The system can now automatically identify crop types from images:

1. **Create a Crop Identification Model on Roboflow:**
   - Go to [Roboflow](https://roboflow.com)
   - Create a new project for crop classification
   - Upload images of healthy leaves for each crop type you want to identify
   - Train a classification model (not object detection)
   - Classes should be: `maize`, `tomato`, `bean`, `potato`, etc.

2. **Configure the Model:**
   - Set `ROBOFLOW_CROP_MODEL_ID` to your crop model's ID
   - Set `ROBOFLOW_CROP_MODEL_VERSION` to your model's version

3. **Use Auto-Identification:**
   - In API calls, set `auto_identify_crop=true` to automatically detect crop type
   - Or use the dedicated `/identify-crop` endpoint

### Weather Integration
- Real-time weather data for farming recommendations
- Location-based temperature analysis

### User Authentication
- JWT-based authentication
- Email verification system

## API Endpoints

### Disease Analysis
```
POST /analyze
```
Parameters:
- `file`: Image file (required)
- `lat`: Latitude (required)
- `lon`: Longitude (required)
- `crop`: Expected crop type (optional)
- `auto_identify_crop`: Enable automatic crop identification (optional, default: false)

### Crop Identification
```
POST /identify-crop
```
Parameters:
- `file`: Image file (required)

Returns crop type and confidence score.

### Debug Endpoint
```
POST /debug/test-disease
```
For testing model predictions.

## Usage Examples

### Basic Disease Analysis
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@maize_leaf.jpg" \
  -F "lat=-1.2864" \
  -F "lon=36.8172" \
  -F "crop=maize"
```

### Auto Crop Identification
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@unknown_crop.jpg" \
  -F "lat=-1.2864" \
  -F "lon=36.8172" \
  -F "auto_identify_crop=true"
```

### Manual Crop Identification
```bash
curl -X POST http://localhost:5000/identify-crop \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@crop_image.jpg"
```

## Model Accuracy & Improvements

### 🎯 Crop Differentiation Accuracy
The system now includes advanced techniques to accurately differentiate between:
- ✅ **Maize leaves** vs Tomato leaves
- ✅ **Bean leaves** vs Potato leaves
- ✅ **Potato leaves** vs Bean leaves
- ✅ **Tomato leaves** vs Maize leaves

### 🔧 Accuracy Improvement Features
- **Image preprocessing** for consistent quality
- **Crop identification pipeline** with confidence scoring
- **Enhanced disease filtering** based on crop type
- **Comprehensive testing tools**

### 📈 Achieving High Accuracy
See `MODEL_ACCURACY_GUIDE.md` for detailed strategies to achieve >95% accuracy.

### 🧪 Testing Your Model
Use `test_crop_identification.py` to evaluate your model's performance:

```bash
python test_crop_identification.py
```

Create a test directory structure:
```
test_images/
├── maize/
├── tomato/
├── bean/
└── potato/
```
