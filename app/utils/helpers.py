import re


def extract_json_from_llm_output(text: str) -> str:
    """
    Extract JSON content from LLM output, removing markdown code blocks if present.
    """
    # Remove Markdown code block if present
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        text = match.group(1)
    # Remove any leading/trailing whitespace
    return text.strip()


def is_preeclampsia_query(query: str) -> bool:
    """
    Check if the query is related to preeclampsia.
    """
    keywords = [
        "preeclampsia", "blood pressure", "proteinuria", "gestational age",
        "hypertension", "pregnancy", "late-onset", "risk factors"
    ]
    return any(word in query.lower() for word in keywords) 