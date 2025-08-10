# Tech Support Assistant Chatbot

A user-friendly technical support chatbot that helps categorize issues and provide step-by-step guidance. It uses a combination of a local dataset and Google’s Gemini API to deliver solutions via a responsive React frontend and Flask backend.

---

##  Dataset
[Kaggle – Tech Support Conversations Dataset](https://www.kaggle.com/datasets/steve1215rogg/tech-support-conversations-dataset)  

---

##  Workflow Overview

1. User enters an issue in the frontend chatbot.
2. Frontend sends request to `Flask` backend (`/chat` endpoint).
3. Backend:
   - Tries to match the issue in the dataset.
   - **If found** → Gemini recomends the best solution from the list.
   - **If not found** → uses **Gemini API** to dynamically generate a solution.
4. Backend formats and sends a clean response to the frontend.
5. Frontend displays the solution interactively.

---

##  Limitations & Notes

- **Dataset-first logic**: If your issue exists in the dataset, Gemini is **not invoked**—only existing dataset solutions are used.
- **Gemini fallback**: If no dataset match, Gemini generates new solutions—quality and response time vary based on server load.
- **Performance variance**:
  - Typical response time: **5–7 seconds**.
  - Under heavy load: up to **40–50 seconds**.
  - Outputs may reflect the current load on Gemini’s servers.

---

##  Tech Stack

- **Backend**: Python, Flask, Pydantic, Gemini API (via `google.generativeai`), Pandas
- **Frontend**: React, Vite, Tailwind CSS, React Router
- **Testing**: Postman for API testing


---

## Sample Prompts

- Software – "The photo editing app crashes every time I try to save a file."

- Account – "I forgot my password and can’t log in to my email."

- Network – "My laptop keeps disconnecting from the Wi-Fi."

- Performance – "My computer takes forever to start up in the morning."

- Hardware – "The keyboard keys are not typing the correct letters."

- Security – "I keep getting a pop-up saying my computer is infected."

- Data/Files – "I accidentally deleted a folder and need to get it back."




## Hosting Setup

This service is hosted on a dedicated server with separate subdomains for frontend and backend APIs:

- **Frontend:** Accessible at [https://techsupport.rafayserver.online](https://techsupport.rafayserver.online)
- **Backend API:** Accessible at [https://api.rafayserver.online](https://api.rafayserver.online)

### Trying the API

You can test the backend API using `curl` or PowerShell:

```powershell
Invoke-RestMethod -Uri "https://api.rafayserver.online/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"my wifi is not working"}'

```

#### Tools Used

- **Docker & Docker Compose** — Containerized deployment for backend and frontend services  
- **Nginx** — Reverse proxy server to route requests to frontend and backend subdomains  
- **Cloudflare** — DNS management and SSL/TLS termination for secure, public access via subdomains  
- **Flask** — Backend web framework powering the API  
- **React & Vite** — Frontend framework and build tool for a fast, modern UI  
- **Gunicorn** — WSGI HTTP server to serve the Flask backend in production  
- **UFW (Uncomplicated Firewall)** — Managed firewall rules on the server (optionally disabled)  
- **Curl & PowerShell** — Tools to test API endpoints from command line  
