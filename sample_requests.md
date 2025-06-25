# Medical AI Assistant - Sample Requests

Complete examples for all endpoints in the Medical AI Assistant API.

## Base URL
```
http://localhost:8000
```

---

## 📋 Documentation Endpoints

### 1. Swagger UI Documentation
```http
GET /docs
```
**Response:** Interactive Swagger UI documentation

### 2. ReDoc Documentation
```http
GET /redoc
```
**Response:** ReDoc documentation interface

### 3. OpenAPI Schema
```http
GET /openapi.json
```
**Response:** Complete OpenAPI JSON schema

---

## 💬 Chat Endpoints

### 1. General Health Questions
```http
POST /chat
Content-Type: application/json

{
  "message": "What are the symptoms of high blood pressure?"
}
```

**Sample Response:**
```json
{
  "response": "High blood pressure symptoms may include headaches, shortness of breath, nosebleeds, and dizziness. However, many people with high blood pressure have no symptoms at all..."
}
```

### 2. Preeclampsia Risk Questions
```http
POST /chat
Content-Type: application/json

{
  "message": "Can you check my preeclampsia risk?"
}
```

**Sample Response:**
```json
{
  "response": "I can help you check your risk of late-onset preeclampsia. To provide an accurate assessment, I need the following 30 variables from your medical tests:\n\n1. Maternal age\n2. Systolic blood pressure\n3. Diastolic blood pressure\n..."
}
```

### 3. Medical Questions
```http
POST /chat
Content-Type: application/json

{
  "message": "What should I know about pregnancy blood pressure monitoring?"
}
```

---

## 🔮 Prediction Endpoints

### 1. Preeclampsia Risk Prediction
```http
POST /predict
Content-Type: application/json

{
  "variables": [
    28.0,     // Maternal age
    120.0,    // Systolic BP
    80.0,     // Diastolic BP
    65.0,     // Weight (kg)
    165.0,    // Height (cm)
    23.8,     // BMI
    0.0,      // Previous preeclampsia (0=No, 1=Yes)
    1.0,      // First pregnancy (0=No, 1=Yes)
    2.5,      // Gestational age (weeks)
    7.2,      // Glucose level
    12.5,     // Hemoglobin
    150000.0, // Platelet count
    1.0,      // Creatinine
    30.0,     // ALT
    25.0,     // AST
    100.0,    // Uric acid
    2.5,      // Protein in urine
    0.0,      // Diabetes (0=No, 1=Yes)
    0.0,      // Hypertension (0=No, 1=Yes)
    0.0,      // Kidney disease (0=No, 1=Yes)
    0.0,      // Autoimmune disease (0=No, 1=Yes)
    1.0,      // Family history (0=No, 1=Yes)
    0.0,      // Smoking (0=No, 1=Yes)
    2.0,      // Number of previous pregnancies
    140.0,    // Fetal heart rate
    98.0,     // Oxygen saturation
    36.5,     // Body temperature
    70.0,     // Pulse rate
    20.0,     // Respiratory rate
    2.8       // Additional clinical parameter
  ]
}
```

**Sample Response:**
```json
{
  "response": "Low risk of late-onset preeclampsia"
}
```

### 2. High Risk Example
```http
POST /predict
Content-Type: application/json

{
  "variables": [
    35.0,     // Maternal age (higher)
    150.0,    // Systolic BP (elevated)
    95.0,     // Diastolic BP (elevated)
    85.0,     // Weight (kg)
    160.0,    // Height (cm)
    33.2,     // BMI (higher)
    1.0,      // Previous preeclampsia (Yes)
    0.0,      // First pregnancy (No)
    28.0,     // Gestational age
    8.5,      // Glucose level (elevated)
    10.8,     // Hemoglobin (lower)
    120000.0, // Platelet count (lower)
    1.4,      // Creatinine (elevated)
    45.0,     // ALT (elevated)
    38.0,     // AST (elevated)
    120.0,    // Uric acid (elevated)
    3.8,      // Protein in urine (elevated)
    1.0,      // Diabetes (Yes)
    1.0,      // Hypertension (Yes)
    0.0,      // Kidney disease
    0.0,      // Autoimmune disease
    1.0,      // Family history (Yes)
    0.0,      // Smoking
    3.0,      // Previous pregnancies
    155.0,    // Fetal heart rate
    96.0,     // Oxygen saturation
    37.2,     // Body temperature
    85.0,     // Pulse rate (elevated)
    22.0,     // Respiratory rate
    3.5       // Additional parameter
  ]
}
```

**Sample Response:**
```json
{
  "response": "High risk of late-onset preeclampsia"
}
```

---

## 🖼️ Image Processing Endpoints

### 1. Extract Variables from Lab Test Image
```http
POST /extract
Content-Type: multipart/form-data

files: [lab_test_image.png]
```

**Using curl:**
```bash
curl -X POST \
  http://localhost:8000/extract \
  -H "Content-Type: multipart/form-data" \
  -F "files=@sample_lab_test.png"
```

**Using Python requests:**
```python
import requests

url = "http://localhost:8000/extract"
with open("sample_lab_test.png", "rb") as f:
    files = {"files": ("sample_lab_test.png", f, "image/png")}
    response = requests.post(url, files=files)
```

**Sample Response (Success):**
```json
{
  "prediction": "Risk of late-onset preeclampsia"
}
```

**Note:** The endpoint processes the image through OpenAI Vision API to extract medical variables, then runs them through the ML prediction model. The response contains only the final prediction result.

**Sample Response (Error - Unsupported Image Format):**
```json
{
  "error": "You uploaded an unsupported image. Please make sure your image has one of the following formats: ['png', 'jpeg', 'gif', 'webp']."
}
```

**Sample Response (Error - OpenAI API Issue):**
```json
{
  "error": "OpenAI API key not configured"
}
```

### 2. Multiple Images Upload
```http
POST /extract
Content-Type: multipart/form-data

files: [image1.png, image2.jpg, image3.png]
```

**Using curl:**
```bash
curl -X POST \
  http://localhost:8000/extract \
  -H "Content-Type: multipart/form-data" \
  -F "files=@image1.png" \
  -F "files=@image2.jpg" \
  -F "files=@image3.png"
```

**Sample Response (Multiple Images):**
```json
{
  "prediction": "High risk of late-onset preeclampsia"
}
```

---

## 🔧 Variable Processing Endpoints

### 1. Normalize Comma-Separated Variables
```http
POST /normalize_variables
Content-Type: application/json

{
  "user_input": "28, 120, 80, 65, 165, 23.8, 0, 1, 2.5, 7.2, 12.5, 150000, 1.0, 30, 25, 100, 2.5, 0, 0, 0, 0, 1, 0, 2, 140, 98, 36.5, 70, 20, 2.8"
}
```

**Sample Response:**
```json
{
  "variables": [28.0, 120.0, 80.0, 65.0, 165.0, 23.8, 0.0, 1.0, 2.5, 7.2, 12.5, 150000.0, 1.0, 30.0, 25.0, 100.0, 2.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2.0, 140.0, 98.0, 36.5, 70.0, 20.0, 2.8]
}
```

### 2. Normalize Natural Language Input
```http
POST /normalize_variables
Content-Type: application/json

{
  "user_input": "I am 28 years old, my blood pressure is 120/80, I weigh 65kg and I'm 165cm tall. This is my first pregnancy."
}
```

### 3. Handle Insufficient Variables
```http
POST /normalize_variables
Content-Type: application/json

{
  "user_input": "28, 120, 80, 65, 165"
}
```

**Sample Response:**
```json
{
  "variables": [28.0, 120.0, 80.0, 65.0, 165.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
```

---

## 🏠 Root Endpoint

### Welcome Message
```http
GET /
```

**Sample Response:**
```json
{
  "message": "Welcome to the Medical AI Assistant API",
  "description": "AI-powered medical assistant for preeclampsia risk assessment",
  "version": "1.0.0",
  "endpoints": {
    "chat": "/chat",
    "prediction": "/predict",
    "image": "/extract",
    "variables": "/normalize_variables",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

---

## 📝 Required Variables for Prediction

The prediction model requires exactly **30 numerical variables** in this order:

1. **Maternal age** (years)
2. **Systolic blood pressure** (mmHg)
3. **Diastolic blood pressure** (mmHg)
4. **Weight** (kg)
5. **Height** (cm)
6. **BMI** (kg/m²)
7. **Previous preeclampsia** (0=No, 1=Yes)
8. **First pregnancy** (0=No, 1=Yes)
9. **Gestational age** (weeks)
10. **Glucose level** (mg/dL)
11. **Hemoglobin** (g/dL)
12. **Platelet count** (per μL)
13. **Creatinine** (mg/dL)
14. **ALT** (U/L)
15. **AST** (U/L)
16. **Uric acid** (mg/dL)
17. **Protein in urine** (g/24h)
18. **Diabetes** (0=No, 1=Yes)
19. **Hypertension** (0=No, 1=Yes)
20. **Kidney disease** (0=No, 1=Yes)
21. **Autoimmune disease** (0=No, 1=Yes)
22. **Family history** (0=No, 1=Yes)
23. **Smoking** (0=No, 1=Yes)
24. **Number of previous pregnancies**
25. **Fetal heart rate** (bpm)
26. **Oxygen saturation** (%)
27. **Body temperature** (°C)
28. **Pulse rate** (bpm)
29. **Respiratory rate** (breaths/min)
30. **Additional clinical parameter**

---

## 🚨 Error Responses

### Validation Error (422)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "message"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### Internal Server Error (500)
```json
{
  "detail": "Internal server error"
}
```

### Image Format Error
```json
{
  "error": "You uploaded an unsupported image. Please make sure your image has one of the following formats: ['png', 'jpeg', 'gif', 'webp']."
}
```

---

## 📊 Supported Image Formats

For the `/extract` endpoint, supported formats are:
- **PNG** (.png)
- **JPEG** (.jpg, .jpeg)
- **GIF** (.gif) 
- **WebP** (.webp)

Maximum file size and other limitations depend on your server configuration. 