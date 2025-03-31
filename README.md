Medical Diagnosis Assistant

Overview

The Medical Diagnosis Assistant is a web-based application designed to analyze patient symptoms and provide medical insights using AI. It consists of a React frontend, a Flask backend, and integrates with Hugging Face APIs for medical analysis.

Features

User-friendly UI with step-by-step patient information and symptom entry.

Real-time form validation and error handling.

AI-powered medical analysis with risk assessments and recommendations.

Dynamic symptom management.

Secure API integration with detailed feedback.

Architecture

Frontend: React, Material-UI

Backend: Flask REST API

AI Integration: Hugging Face API

Installation

Clone the repository:

git clone https://github.com/mukthaparam/medical-diagnosis-assistant.git

Install Dependencies:

cd frontend
npm install
cd ../backend
pip install -r requirements.txt

Run the Application:

# Start frontend
cd frontend
npm start

# Start backend
cd ../backend
python app.py

API Endpoint

POST /api/analyze

Input: { symptoms: [], patient_info: {} }

Output: Medical insights with recommendations.

Error Handling

Form Validation on frontend.

Detailed error messages from the backend.

Proper HTTP status codes.

Future Enhancements

User authentication

EHR integration

Multilingual support

Mobile application

Data visualization

License

This project is licensed under the MIT License.
