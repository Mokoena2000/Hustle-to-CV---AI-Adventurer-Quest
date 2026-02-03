# Hustle-to-CV---AI-Adventurer-Quest

Hustle-to-CV
Project Overview
Hustle-to-CV is a full-stack web application designed to help workers in the informal sector transform their daily work experience into professional, industry-standard CV bullet points. The application uses AI to bridge the gap between informal labor and formal employment documentation.

Tech Stack
Frontend: React with TypeScript, Vite, and Tailwind CSS.

Backend: FastAPI (Python) for the REST API.

Database: SQLModel with SQLite for data persistence.

Authentication: Clerk for user management and secure session handling.

AI Integration: OpenRouter API (OpenAI-compatible client).

Icons: Lucide-React.

Application Logic
User Authentication: Users sign in via Clerk. The frontend retrieves a JWT token to authorize requests to the backend.

Data Input: The user enters raw descriptions of their work (e.g., "taxi driver for 5 years") into a React form.

Backend Processing:

The FastAPI server receives the POST request.

It validates the data shape using Pydantic/SQLModel.

It sends the raw text to an AI service (OpenRouter).

Data Persistence: * The backend checks if the user exists in the SQLite database via their email.

If they exist, it updates their profile with the new AI-generated CV.

If not, it creates a new record with a unique identifier.

Response: The frontend receives the formatted text and displays it to the user with a "Copy to Clipboard" feature.

Development Progress
The project is currently in the late-stage integration phase.

The Frontend-to-Backend communication is fully established and verified.

The Database Layer is functional, successfully handling record creation and updates.

CORS and Middleware configurations are resolved, allowing seamless local cross-origin requests.

Error Handling has been implemented on both sides to provide clear feedback during failures.

Current Blocker
The primary remaining blocker is an External API Authentication Error (401 Unauthorized) from the OpenRouter service.

Observation: The backend logic successfully triggers the AI service call, but the service returns a "User not found" error.

Status: This has been narrowed down to an issue with the API key configuration or account credits on the provider side.

Verification: The backend "Partial Success" state confirms that all internal code (FastAPI, SQLModel, React) is working as intended; the application is simply waiting for a valid external service handshake to flow the data.

Setup Instructions
Backend

Navigate to /backend.

Install dependencies: pip install -r requirements.txt.

Run server: uvicorn app.main:app --reload --port 8080.

Frontend

Navigate to /frontend.

Install dependencies: npm install.

Run app: npm run dev.