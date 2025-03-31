from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.diagnosis import analyze_symptoms

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        symptoms = data.get('symptoms', [])
        patient_info = data.get('patient_info', {})
        
        # Get AI analysis
        diagnosis = analyze_symptoms(symptoms, patient_info)
        
        return jsonify({
            'success': True,
            'diagnosis': diagnosis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True) 