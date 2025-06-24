from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from app.core.config import OPENAI_API_KEY
from app.models.ml_models import preeclampsia_model


# LangChain LLM setup - only initialize if API key is available
llm = None
agent = None

if OPENAI_API_KEY:
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    def general_healthcare_qa(query: str) -> str:
        """General LLM tool for healthcare Q&A"""
        system_prompt = (
            "You are a helpful and knowledgeable medical assistant. "
            "Provide detailed, clear, and informative answers to healthcare questions. "
            "Your responses should be about 200 words long, unless the question is very simple."
        )
        return llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ])

    # Define tools for LangChain
    llm_tool = Tool(
        name="General Healthcare QA",
        func=general_healthcare_qa,
        description="Answers general healthcare and medical questions."
    )

    preeclampsia_tool = Tool(
        name="preeclampsia_predictor",
        func=lambda x: preeclampsia_model.predict([float(i) for i in x.split(",")]),
        description="Predicts late-onset preeclampsia from patient variables. Input should be a comma-separated list of floats."
    )

    tools = [preeclampsia_tool, llm_tool]

    # Initialize the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )