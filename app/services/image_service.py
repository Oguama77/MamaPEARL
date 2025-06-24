import base64
import json
from typing import List
from openai import OpenAI
from app.core.config import OPENAI_API_KEY, VARIABLE_LIST, MEAN_VALUES
from app.utils.helpers import extract_json_from_llm_output


class ImageProcessingService:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    async def extract_variables_from_images(self, image_files) -> dict:
        """Extract medical variables from uploaded images"""
        if not self.client:
            return {"success": False, "error": "OpenAI API key not configured"}
            
        image_b64_list = []
        for file in image_files:
            image_bytes = await file.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            image_b64_list.append(image_b64)

        prompt = (
            "From the provided medical test result images, extract the numerical values for the following variables. "
            "If a variable is not present, use 'null'. Return the result as a JSON object where the keys are the variable names "
            f"from this list: {', '.join(VARIABLE_LIST)}. "
            "For example: {\"Gestational age\": 34, \"Albumin level\": 3.5, ...}"
        )

        # Compose the content for all images
        content = [{"type": "text", "text": prompt}]
        for image_b64 in image_b64_list:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}})

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a medical assistant that extracts structured data from images."},
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=512
        )
        
        raw_output = response.choices[0].message.content
        json_str = extract_json_from_llm_output(raw_output)
        
        try:
            extracted = json.loads(json_str)
            # Fill missing/null values with means
            final_values = []
            for i, var in enumerate(VARIABLE_LIST):
                val = extracted.get(var)
                if val is None or (isinstance(val, str) and val.lower() == "null"):
                    final_values.append(MEAN_VALUES[i])
                else:
                    try:
                        final_values.append(float(val))
                    except Exception:
                        final_values.append(MEAN_VALUES[i])
            
            return {"success": True, "variables": final_values}
        except Exception as e:
            return {"success": False, "error": f"Could not parse output as JSON: {json_str}. Error: {e}"}


# Initialize the service
image_service = ImageProcessingService() 