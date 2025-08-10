import pandas as pd
from google import genai
import json
import re
from pydantic import BaseModel, ValidationError
from flask import Flask, request, jsonify
from flask_cors import CORS


GEMINI_API = 'AIzaSyAru93hlGb1Pa5kicyZ1a58A4ZjCMxveok'
app = Flask(__name__)

CORS(app,origins=["https://localhost:5173"])



def process_issue(CUSTOMER_ISSUE):
    prompt = f"""You are a technical support assistant.
    Your job is to:

    Step 1 – Find the Closest Issue
    From this list:

    Cannot connect to Wi-Fi 

    Software installation failure 

    Forgot password 

    Unable to access email 

    Blue screen error 

    Printer not responding 

    Slow system performance 

    Choose the one that is most similar in meaning to the customer’s issue.
    Do not choose “Slow system performance” unless the issue is clearly about speed, freezing, lag, or slowness without a specific error code.

    Step 2 – Assign the Category
    Categories:

    Software – Problems with installing, updating, or using apps/programs.

    Account – Login, password, or account access problems.

    Network – Internet or Wi-Fi connectivity issues.

    Performance – Slow speed, freezing, crashing, or blue screen errors.

    Hardware – Issues with physical devices or components.

    Security – Virus alerts, suspicious pop-ups, or password breaches.

    Data/Files – Missing files, file recovery, or problems opening documents.

    Tie-Break Rules:

    If there is a specific error mentioned (e.g., “blue screen”), choose that exact issue.

    If the problem is about a device not working physically, choose a Hardware issue.

    If the problem is about network connectivity, choose Network.

    If it’s about installing/running software and not about performance, choose Software.

    If it’s about login or account recovery, choose Account.

    Respond ONLY in valid JSON format like this:
    {{"closestissue": "<exact issue>", "category": "<category name>"}}

    Balanced Examples:

    Customer Issue: "My laptop freezes and shows a blue error screen after 10 minutes"
    Closest Issue: Blue screen error
    Category: Performance

    Customer Issue: "Cannot connect to the office internet"
    Closest Issue: Cannot connect to Wi-Fi
    Category: Network

    Customer Issue: "I forgot my email password and can’t log in"
    Closest Issue: Forgot password
    Category: Account

    Customer Issue: "The antivirus installation fails with an error"
    Closest Issue: Software installation failure
    Category: Software

    Customer Issue: "The printer won’t print anything"
    Closest Issue: Printer not responding
    Category: Hardware

    Customer Issue: "My PC is very slow when opening programs"
    Closest Issue: Slow system performance
    Category: Performance

    Customer Issue: "My email app crashes every time I open it"
    Closest Issue: Unable to access email
    Category: Account

    Now classify:
    Customer Issue: "{CUSTOMER_ISSUE}"

    """

    client = genai.Client(api_key= GEMINI_API)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents= prompt)

    return response


def parse_response(response):
    class SupportClassification(BaseModel):
        closestissue: str
        category: str

    response_text = response.candidates[0].content.parts[0].text.strip()

    match = re.search(r"\{[\s\S]*\}", response_text)
    if not match:
        raise ValueError("No JSON object found in the response.")

    json_str = match.group(0)

    try:
        parsed = SupportClassification(**json.loads(json_str))
        print("Closest Issue:", parsed.closestissue)
        print("Category:", parsed.category)

        return (parsed.closestissue,parsed.category)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
    except ValidationError as e:
        print("Pydantic validation error:", e)



def generate_solution(closestissue,category,CUSTOMER_ISSUE):
    df = pd.read_csv(r'tech_support_dataset.csv')

    if category in ['Software' ,'Account', 'Network' ,'Performance' ,'Hardware']:
        filtered = df[(df['Issue_Category'] == category) & (df['Customer_Issue'] == closestissue)]
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

    Respond ONLY in this format (no extra text) using exactly this shape:
    
    "category": "{category}",
    "used_fallback": <true|false>,
    "solution_steps": ["<step1>", "<step2>", "..."]
    
    """
# {{
#     "customer_issue": "{CUSTOMER_ISSUE}",
#     "closestissue": "{closestissue}",
#     "category": "{category}",
#     "used_fallback": <true|false>,
#     "solution_steps": ["<step1>", "<step2>", "..."]
#     }}

    client = genai.Client(api_key= GEMINI_API)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents= prompt
    )

    return response.text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query','')

    if not query:
        return jsonify({'error':'No query provided'}) , 400
    
    
    try:
        resp1 = process_issue(query)
        issue,category = parse_response(response=resp1)
        print(issue , category)
        resp2 = generate_solution(issue,category,query)
        print(resp2)
        return jsonify({'response': resp2})
    except Exception as e:
        return jsonify({'error' : str(e)} , 500)



if __name__ == '__main__':

    app.run(host='0.0.0.0' , port=5173)

    