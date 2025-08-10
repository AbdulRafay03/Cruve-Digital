from google import genai
import json
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API = os.getenv('GEMINI_API')
if not GEMINI_API:
    raise RuntimeError("Missing GEMINI API KEY envoirment variable")


class Process_issue:

    def __init__(self):
        self.client = genai.Client(api_key= GEMINI_API)
        

    def process_issue(self,CUSTOMER_ISSUE):
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
        response = self.client.models.generate_content(
        model="gemini-2.5-flash", contents= prompt)

        return response
