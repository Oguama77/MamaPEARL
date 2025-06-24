import joblib
from app.core.config import MODEL_PATH, SCALER_PATH


class PreeclampsiaModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load the pre-trained model and scaler"""
        with open(MODEL_PATH, "rb") as f:
            self.model = joblib.load(f)
        with open(SCALER_PATH, "rb") as f:
            self.scaler = joblib.load(f)
    
    def predict(self, variables):
        """Make prediction using the loaded model"""
        scaled_vars = self.scaler.transform([variables])
        pred = self.model.predict(scaled_vars)[0]
        
        if pred == 0:
            return "No risk of late-onset preeclampsia"
        elif pred == 1:
            return "Risk of late-onset preeclampsia"
        else:
            return f"Model output: {pred}"


# Initialize the model instance
preeclampsia_model = PreeclampsiaModel()