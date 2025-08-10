import pandas as pd
from google import genai
import json
from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API = os.getenv('GEMINI_API')
if not GEMINI_API:
    raise RuntimeError("Missing GEMINI API KEY envoirment variable")


class response_generator:

    def __init__(self):        
        self.df = pd.read_csv(r'tech_support_dataset.csv')
        self.client = genai.Client(api_key= GEMINI_API)\
    

    def generate_solution(self,closestissue,category,CUSTOMER_ISSUE):
        
        if category in ['Software' ,'Account', 'Network' ,'Performance' ,'Hardware']:
            filtered = self.df[(self.df['Issue_Category'] == category) & (self.df['Customer_Issue'] == closestissue)]
            SOLUTIONS = filtered['Tech_Response'].unique()
        else:
            SOLUTIONS = None

        prompt = f"""
            You are a technical support assistant.

            Customer Issue: "{CUSTOMER_ISSUE}"
            Closest Issue: "{closestissue}"
            Category: "{category}"

            You are given an array of possible solutions:
            {SOLUTIONS}
            If array is NULL you may GENERATE solution steps.

            Task:
            1. From the provided array, PICK the single most relevant solution and produce a short, logical step-by-step plan (2–6 steps) using only solutions from the provided array.
            2. If NONE of the provided solutions are relevant, you MAY GENERATE a concise fallback step-by-step guide (3–6 steps). Only generate a fallback when absolutely necessary.
            3. Do NOT invent or add extra solutions if at least one provided solution applies.
            4. If you generate a fallback guide, set "used_fallback": true. Otherwise set "used_fallback": false.

            Respond ONLY JSON format (no extra text) using exactly this shape:
            {{
            "category": "{category}",
            "used_fallback": <true|false>,
            "solution_steps": ["<step1>", "<step2>", "..."]
            }}
            """

        

        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents= prompt
        )

        return response.text