from fastapi import APIRouter
from app.schemas.requests import ChatInput
from app.services.agent_service import agent
from app.core.config import VARIABLE_LIST

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(data: ChatInput):
    """Handle chat messages and provide medical assistance"""
    
    # Let the LLM classify the user's intent instead of using keywords
    if not agent:
        return {"response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable to use this feature."}
    
    # First, classify the user's intent
    intent_prompt = f"""
    Analyze this user message and determine their intent. Respond with only one word:
    - "RISK_ASSESSMENT" if they want to check/assess/predict their preeclampsia risk (need medical variables)
    - "INFORMATION" if they want general information about preeclampsia (symptoms, causes, treatment, etc.)
    - "GENERAL" for any other healthcare or non-healthcare questions
    
    User message: "{data.message}"
    
    Intent:"""
    
    try:
        intent_response = agent.invoke({"input": intent_prompt})
        intent = intent_response["output"].strip().upper()
        
        if intent == "RISK_ASSESSMENT":
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
            # Handle general healthcare questions and informational requests
            response = agent.invoke({"input": data.message})
            return {"response": response["output"]}
            
    except Exception as e:
        # Fallback to general response if intent classification fails
        response = agent.invoke({"input": data.message})
        return {"response": response["output"]} 