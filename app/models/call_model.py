import os
import joblib
from app.core.config import MODEL_PATH, SCALER_PATH, POSTGRES_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()


engine = create_engine(POSTGRES_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Attempt to connect to the database and print a message
try:
    with engine.connect() as connection:
        print("[DB] Successfully connected to the PostgreSQL database.")
except Exception as e:
    print(f"[DB] Failed to connect to the PostgreSQL database: {e}")


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