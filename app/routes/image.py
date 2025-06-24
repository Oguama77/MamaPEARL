from fastapi import APIRouter, File, UploadFile
from typing import List
from app.services.image_service import image_service
from app.models.ml_models import preeclampsia_model

router = APIRouter()


@router.post("/extract")
async def extract_variables(files: List[UploadFile] = File(...)):
    """Extract variables from medical test result images and make prediction"""
    result = await image_service.extract_variables_from_images(files)
    
    if result["success"]:
        # Make prediction with extracted variables
        prediction = preeclampsia_model.predict(result["variables"])
        return {"prediction": prediction}
    else:
        return {"error": result["error"]} 