from fastapi import APIRouter
from app.schemas.requests import FormInput
from app.models.ml_models import preeclampsia_model

router = APIRouter()


@router.post("/predict")
async def predict_endpoint(data: FormInput):
    """Make preeclampsia prediction using ML model"""
    response = preeclampsia_model.predict(data.variables)
    return {"response": response} 