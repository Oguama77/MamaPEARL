from fastapi import APIRouter, Body
from app.services.variable_service import variable_service

router = APIRouter()


@router.post("/normalize_variables")
async def normalize_variables(user_input: str = Body(..., embed=True)):
    """Normalize user input variables for ML model"""
    result = variable_service.normalize_variables(user_input)
    
    if result["success"]:
        return {"variables": result["variables"]}
    else:
        return {"error": result["error"]} 