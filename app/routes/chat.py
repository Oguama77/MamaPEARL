from fastapi import APIRouter
from app.schemas.requests import ChatInput
from app.services.agent_service import agent
from app.core.config import VARIABLE_LIST

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(data: ChatInput):
    """Handle chat messages and provide medical assistance"""
    # Check if user is asking about preeclampsia risk specifically
    preeclampsia_keywords = [
        "preeclampsia", "preeclampsia risk", "risk of preeclampsia", 
        "check preeclampsia", "preeclampsia prediction", "late-onset preeclampsia"
    ]
    
    is_asking_about_risk = any(keyword in data.message.lower() for keyword in preeclampsia_keywords)
    
    if is_asking_about_risk:
        response_text = (
            "I can help you check your risk of late-onset preeclampsia. "
            "To provide an accurate assessment, I need the following 30 variables from your medical tests:\n\n"
        )
        
        for i, var in enumerate(VARIABLE_LIST, 1):
            response_text += f"{i}. {var}\n"
        
        response_text += (
            "\nPlease provide these values as comma-separated numbers in the order listed above. "
            "You can also upload an image of your test results using the 'Extract Variables from Test Result Image' feature above."
        )
        
        return {"response": response_text}
    else:
        # Handle general healthcare questions
        if not agent:
            return {"response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable to use this feature."}
        response = agent.invoke({"input": data.message})
        return {"response": response["output"]} 