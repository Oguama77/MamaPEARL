import os

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if OPENAI_API_KEY:
#     OPENAI_API_KEY = OPENAI_API_KEY.strip()
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"

# Mean values for missing variables
MEAN_VALUES = [
    30.383824, 0.047224, 2.114673, 59.325487, 13.121650, 16.193501, 5.908047, 5.209185, 149.911673, 0.410707,
    5.840941, 3.739687, 9.714550, 66.197603, 2.134625, 2.607922, 0.070634, 199.839308, 0.281055, 13.475048,
    3.761391, 2.503311, 31.665389, 0.203468, 8.857324, 111.964249, 67.989443, 963.371447, 160.779131, 60.139828, 58.334186
]

# Variable list for medical prediction
VARIABLE_LIST = [
    "Gestational age", "Albumin level", "Alkaline phosphate level",
    "Alanine transaminase level", "Aspartate transaminase level", "Blood urea nitrogen level",
    "Calcium level", "Cholesterol level", "Serum creatinine level", "C-reactive protein level",
    "Erythrocyte sedimentation rate", "Gamma-glutamyl transferase (GGT) level", "Glucose level",
    "Hemoglobin", "Potassium", "Magnesium", "Platelet count", "Total bilirubin",
    "Total CO2 (bicarbonate)", "Total protein", "Uric acid",
    "Urine albumin-to-creatinine ration", "Urine protein/creatinine ratio",
    "White blood cell count", "Systolic blood pressure", "Diastolic blood pressure",
    "Protein level in urine", "Height (cm)", "Maternal weight at pregnancy (kg)", "Fundal height (cm)"
] 