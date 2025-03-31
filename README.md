# Medical Diagnosis Assistant System

An AI-driven solution that helps streamline the initial patient diagnosis process in healthcare settings.

## Features

- Patient symptom collection and analysis
- AI-powered preliminary diagnosis suggestions
- Structured medical report generation
- User-friendly web interface

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the backend:
```bash
python backend/app.py
```

4. Run the frontend:
```bash
cd frontend
npm install
npm start
```

## Project Structure

- `backend/`: Flask API server
- `frontend/`: React web application
- `models/`: AI models and utilities
- `data/`: Training and reference data

## Technology Stack

- Backend: Python, Flask
- Frontend: React, Material-UI
- AI: OpenAI GPT, scikit-learn
- Database: SQLite (for development) 