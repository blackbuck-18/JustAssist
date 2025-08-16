JustAssist ⚖️🤖
JustAssist is an AI-powered legal aid assistant designed to democratize access to legal information in India. It provides clear, accurate, and easy-to-understand answers to legal queries based on official government documents, helping citizens understand and exercise their rights.

This project directly supports the United Nations' Sustainable Development Goal 16 (SDG 16): Peace, Justice, and Strong Institutions.

🚀 Features
Multi-Domain Knowledge: The AI is an expert in several key areas of Indian law, including:

The Right to Information (RTI) Act

The Consumer Protection Act

The Indian Contract Act

Landlord-Tenant laws (The Transfer of Property Act)

Smart Router: An intelligent routing system that understands the user's query and directs it to the correct legal knowledge base for the most accurate answers.

Retrieval-Augmented Generation (RAG): The AI provides answers based only on the content of official legal documents, preventing hallucinations and ensuring the information is trustworthy.

User-Friendly Interface: A clean, modern, and responsive web interface with a landing page and a dedicated chat page.

🛠️ Tech Stack
Frontend: HTML5, CSS3, JavaScript

Backend: Python with FastAPI

AI Core:

Framework: LangChain

LLM: Google Gemini

Vector Database: ChromaDB

Deployment:

Frontend: Vercel

Backend: Render

⚙️ Local Setup and Installation
To run this project on your local machine, follow these steps:

Prerequisites
Python 3.10+

Node.js (for frontend development, if needed)

A Google Gemini API Key

Backend Setup
Navigate to the backend directory:

cd backend

Create and activate a virtual environment:

# Create
python -m venv venv
# Activate (Windows)
.\venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Create a .env file and add your API key:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"

Run the knowledge base setup script (only needs to be run once):

python setup_knowledge_base.py

Start the server:

uvicorn main:app --reload

The backend will be running at http://127.0.0.1:8000.

Frontend Setup
Navigate to the frontend directory.

Open the index.html file in your web browser.

👥 Developed By
TEAM: 5-STAR ARCHITECTS
S. SRI ADITHYA

B. KRISHNA CHAITANYA

B. HEMANTH VENKAT RAGHU

G. PRAHALAD

M. HEMANTH KUMAR REDDY
