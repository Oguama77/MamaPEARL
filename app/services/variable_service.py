from app.core.config import VARIABLE_LIST, MEAN_VALUES, OPENAI_API_KEY
from langchain_openai import ChatOpenAI


class VariableService:
    def __init__(self):
        self.llm = None
        if OPENAI_API_KEY:
            self.llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    def normalize_variables(self, user_input: str) -> dict:
        """Normalize user input variables using LLM"""
        if not self.llm:
            return {"success": False, "error": "OpenAI API key not configured"}
            
        prompt = (
            "You are a medical assistant. The user will provide a list of variable names and values, possibly unordered and incomplete. "
            "Here is the required variable list, in order:\n"
            + "\n".join([f"{i+1}. {name}" for i, name in enumerate(VARIABLE_LIST)]) +
            "\n\nHere are the mean values for each variable, in order:\n"
            + ", ".join(str(x) for x in MEAN_VALUES) +
            "\n\nGiven the user's input:\n" + user_input +
            "\n\nReturn a comma-separated list of 30 values in the correct order, using the user's values where available, and the mean for any missing variable. Output only the comma-separated list of 30 values."
        )
        
        result = self.llm.invoke([
            {"role": "system", "content": "You are a medical assistant that arranges variables for a machine learning model."},
            {"role": "user", "content": prompt}
        ])
        
        # Parse the result into a list of floats
        try:
            values = [float(x.strip()) for x in result.content.split(",") if x.strip()]
            if len(values) != 30:
                return {"success": False, "error": f"Expected 30 values, got {len(values)}. Output: {result.content}"}
            return {"success": True, "variables": values}
        except Exception as e:
            return {"success": False, "error": f"Could not parse output: {result.content}. Error: {e}"}


# Initialize the service
variable_service = VariableService() 