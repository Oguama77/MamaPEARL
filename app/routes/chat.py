from fastapi import APIRouter, Depends
from app.schemas.requests import ChatInput
from app.services.agent_service import agent
from app.core.config import VARIABLE_LIST
from app.models import ChatSession, ChatMessage
from app.models.ml_models import SessionLocal
from sqlalchemy.orm import Session
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat")
async def chat_endpoint(data: ChatInput, db: Session = Depends(get_db)):
    """Handle chat messages and provide medical assistance with DB-backed context."""
    if not agent:
        return {"response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable to use this feature."}

    # Fetch the session
    session = db.query(ChatSession).filter(ChatSession.id == data.session_id).first()
    if not session:
        return {"response": "Invalid session_id. Please start a new session."}
    user_id = session.user_id

    # Fetch all messages for this session, ordered by created_at
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == data.session_id).order_by(ChatMessage.created_at).all()

    # Build conversation context for the LLM
    conversation = []
    for msg in messages:
        role = "user" if msg.type == "user" else "assistant"
        conversation.append({"role": role, "content": msg.content})
    # Add the new user message
    conversation.append({"role": "user", "content": data.message})

    # Classify the user's intent
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
            assistant_reply = response_text
        else:
            # Use conversation context for general/informational questions
            response = agent.llm.invoke(conversation)
            assistant_reply = response.content if hasattr(response, 'content') else response["output"]
        # Store the new user message
        user_msg = ChatMessage(
            session_id=data.session_id,
            user_id=user_id,
            type="user",
            content=data.message,
            created_at=datetime.datetime.utcnow()
        )
        db.add(user_msg)
        # Store the assistant's reply
        assistant_msg = ChatMessage(
            session_id=data.session_id,
            user_id=user_id,
            type="assistant",
            content=assistant_reply,
            created_at=datetime.datetime.utcnow()
        )
        db.add(assistant_msg)
        # Update session's updated_at
        session.updated_at = datetime.datetime.utcnow()
        db.commit()
        return {"response": assistant_reply}
    except Exception as e:
        db.rollback()
        return {"response": f"An error occurred: {str(e)}"} 