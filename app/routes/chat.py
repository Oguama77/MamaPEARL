from fastapi import APIRouter
from app.schemas.requests import ChatInput
from app.services.agent_service import agent
from app.core.config import VARIABLE_LIST

# Langchain imports for memory
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from app.core.config import OPENAI_API_KEY

router = APIRouter()

# In-memory store for user conversation memories
user_memories = {}

def get_user_memory(user_id: str):
    """Retrieve or create a ConversationSummaryMemory for a user."""
    if user_id not in user_memories:
        llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo"
        )
        user_memories[user_id] = ConversationSummaryMemory(
            llm=llm,
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[user_id]

@router.post("/chat")
async def chat_endpoint(data: ChatInput):
    """Handle chat messages and provide medical assistance with context memory."""
    
    if not agent:
        return {"response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable to use this feature."}
    
    # Get or create the user's conversation memory
    memory = get_user_memory(data.user_id)

    # Classify the user's intent
    intent_prompt = f"""
    Analyze this user message and determine their intent. Respond with only one word:
    - "RISK_ASSESSMENT" if they want to check/assess/predict their preeclampsia risk (need medical variables)
    - "INFORMATION" if they want general information about preeclampsia (symptoms, causes, treatment, etc.)
    - "GENERAL" for any other healthcare or non-healthcare questions
    
    User message: "{data.message}"
    
    Intent:"""
    try:
        # Use memory to summarize previous conversation for context
        summary = memory.load_memory_variables({}).get("chat_history", "")
        # Prepend summary/context to the prompt
        context_message = f"Previous conversation summary: {summary}\nUser: {data.message}" if summary else data.message
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
            # Save the interaction to memory
            memory.save_context({"input": data.message}, {"output": response_text})
            return {"response": response_text}
        else:
            # Handle general healthcare questions and informational requests
            # Use memory for context
            llm = ChatOpenAI(
                temperature=0.7,
                openai_api_key=OPENAI_API_KEY,
                model="gpt-3.5-turbo"
            )
            # Compose the prompt with context
            prompt = f"Previous conversation summary: {summary}\nUser: {data.message}" if summary else data.message
            response = llm.invoke([
                {"role": "system", "content": "You are a friendly and knowledgeable medical AI assistant. You help users with healthcare-related questions and general conversation."},
                {"role": "user", "content": prompt}
            ])
            memory.save_context({"input": data.message}, {"output": response.content})
            return {"response": response.content}
    except Exception as e:
        # Fallback to general response if intent classification fails
        llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo"
        )
        prompt = f"Previous conversation summary: {summary}\nUser: {data.message}" if summary else data.message
        response = llm.invoke([
            {"role": "system", "content": "You are a friendly and knowledgeable medical AI assistant. You help users with healthcare-related questions and general conversation."},
            {"role": "user", "content": prompt}
        ])
        memory.save_context({"input": data.message}, {"output": response.content})
        return {"response": response.content} 