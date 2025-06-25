from langchain_openai import ChatOpenAI
from app.core.config import OPENAI_API_KEY


# Simple LLM setup for better conversational experience
llm = None

if OPENAI_API_KEY:
    llm = ChatOpenAI(
        temperature=0.7,  # Slightly more creative for conversation
        openai_api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo"
    )


def get_chat_response(message: str) -> str:
    """Get a conversational response from the AI assistant"""
    if not llm:
        return "I'm sorry, I'm not configured to respond right now. Please check the API configuration."
    
    # Define the system prompt for the medical assistant
    system_prompt = """You are a friendly and knowledgeable medical AI assistant. You help users with healthcare-related questions and general conversation.

Key guidelines:
- Be conversational and friendly
- For greetings like "hi", "hello", respond naturally and ask how you can help
- For medical questions, provide helpful, accurate information
- For non-medical questions, politely redirect to healthcare topics while still being helpful
- Keep responses concise but informative
- Always encourage users to consult healthcare professionals for medical advice
"""
    
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your message. Please try again."


# Create a simple agent interface for backward compatibility
class SimpleAgent:
    def invoke(self, input_dict):
        message = input_dict.get("input", "")
        response = get_chat_response(message)
        return {"output": response}


# Initialize the agent
agent = SimpleAgent() if OPENAI_API_KEY else None