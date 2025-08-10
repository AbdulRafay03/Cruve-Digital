from pydantic import BaseModel, ValidationError
import re
import json

class SupportClassification(BaseModel):
    closestissue: str
    category: str

class SupportClassifier:
    def __init__(self):
        pass 

    def parse_response(self, response: str):
        response_text = response.candidates[0].content.parts[0].text.strip()

        # Try to extract JSON inside curly braces
        match = re.search(r"\{[\s\S]*\}", response_text)
        if not match:
            raise ValueError("No JSON object found in the response.")

        json_str = match.group(0)

        try:
            parsed = SupportClassification(**json.loads(json_str))
            print("Closest Issue:", parsed.closestissue)
            print("Category:", parsed.category)

            return parsed.closestissue,parsed.category
        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
        except ValidationError as e:
            print("Pydantic validation error:", e)
