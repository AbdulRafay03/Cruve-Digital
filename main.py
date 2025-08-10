import pandas as pd
from google import genai
import json
import re
from pydantic import BaseModel, ValidationError
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from process_issue import Process_issue
from response_parser import SupportClassifier
from response_generator import response_generator


load_dotenv()
GEMINI_API = os.getenv('GEMINI_API')
if not GEMINI_API:
    raise RuntimeError("Missing GEMINI API KEY envoirment variable")


app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "*"}}) 


@app.route('/api/healthcheck')
def healthcheck():
    return {"status": "ok"}, 200

@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()
    query = data.get('query','')

    if not query:
        return jsonify({'error':'No query provided'}) , 400
    
    print(query)
    
    try:
        resp1 = pro_issue.process_issue(query)
        
        issue,category = res_par.parse_response(response=resp1)
        print(issue , category)

        # print("Calling generate_solution with:", issue, category, query)
        resp2 = res_gen.generate_solution(issue,category,query)
        print(resp2)
        

        try:
            # Extract JSON part from resp2 if it's wrapped in code fences
            match = re.search(r"\{[\s\S]*\}", resp2)
            if match:
                resp2 = match.group(0)

            # Parse JSON safely
            solution_data = json.loads(resp2.strip())

            # Format output
            steps_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(solution_data["solution_steps"]))
            formatted_response = f"Category: {solution_data['category'].title()}\nSteps:\n{steps_text}"
            return jsonify({"response": formatted_response})

        except json.JSONDecodeError:
            
            return jsonify({"response": resp2})
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error' : str(e)} , 500)




if __name__ == '__main__':

    pro_issue = Process_issue()
    res_par = SupportClassifier()
    res_gen = response_generator()

    app.run(host='0.0.0.0' , port=8000)

    