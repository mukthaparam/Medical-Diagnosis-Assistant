import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

# Hugging Face API endpoint - using a medical-focused model
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def analyze_symptoms(symptoms: List[str], patient_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze patient symptoms using Hugging Face's model to provide preliminary diagnosis.
    
    Args:
        symptoms (List[str]): List of patient symptoms
        patient_info (Dict[str, Any]): Patient information including age, gender, etc.
    
    Returns:
        Dict[str, Any]: Analysis results including possible conditions and recommendations
    """
    # Prepare the prompt for the model
    prompt = f"""
    Medical Case Analysis:
    Patient Demographics:
    - Age: {patient_info.get('age', 'Not provided')}
    - Gender: {patient_info.get('gender', 'Not provided')}
    - Medical History: {patient_info.get('medical_history', 'Not provided')}
    
    Presenting Symptoms:
    {', '.join(symptoms)}
    
    Please provide a detailed medical analysis including:
    1. Differential diagnosis
    2. Risk factors
    3. Potential complications
    4. Recommended diagnostic tests
    5. Treatment considerations
    """
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Call Hugging Face API
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"inputs": prompt}
            )
            
            if response.status_code == 503:
                if attempt < max_retries - 1:
                    print(f"Model is loading, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    return generate_detailed_analysis(symptoms, patient_info)
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status code {response.status_code}")
            
            # Parse and structure the response
            analysis = response.json()[0]['summary_text']
            
            # Analyze medical history
            history_analysis = analyze_medical_history(patient_info.get('medical_history', ''))
            
            # Format the response with detailed medical analysis
            formatted_analysis = f"""
            Medical Analysis Report
            ======================
            
            Patient Information:
            -------------------
            Age: {patient_info.get('age', 'Not provided')}
            Gender: {patient_info.get('gender', 'Not provided')}
            
            Medical History Analysis:
            -----------------------
            {history_analysis['summary']}
            
            Presenting Symptoms:
            ------------------
            {', '.join(symptoms)}
            
            Clinical Assessment:
            ------------------
            1. Differential Diagnosis:
               {analysis}
            
            2. Risk Assessment:
               - Age-related factors: {get_age_risk_factors(patient_info.get('age'))}
               - Gender-specific considerations: {get_gender_considerations(patient_info.get('gender'))}
               - Medical history impact: {history_analysis['risk_factors']}
            
            3. Potential Complications:
               - Acute complications: {get_acute_complications(symptoms)}
               - Chronic implications: {get_chronic_implications(symptoms)}
               - History-related complications: {history_analysis['complications']}
            
            4. Recommended Diagnostic Workup:
               - Initial screening tests: {get_screening_tests(symptoms)}
               - Additional investigations: {get_additional_tests(symptoms)}
               - History-specific tests: {history_analysis['recommended_tests']}
            
            5. Treatment Considerations:
               - Immediate interventions: {get_immediate_interventions(symptoms)}
               - Long-term management: {get_long_term_management(symptoms)}
               - History-based precautions: {history_analysis['precautions']}
            
            6. Follow-up Recommendations:
               - Monitoring parameters: {get_monitoring_parameters(symptoms)}
               - Referral criteria: {get_referral_criteria(symptoms)}
               - History-specific monitoring: {history_analysis['monitoring']}
            
            7. Lifestyle Recommendations:
               - Diet and nutrition: {get_diet_recommendations(symptoms, patient_info)}
               - Exercise guidelines: {get_exercise_recommendations(symptoms, patient_info)}
               - Stress management: {get_stress_management(symptoms, patient_info)}
            
            Important Notes:
            --------------
            - This is an AI-generated preliminary analysis and should not replace professional medical evaluation
            - Seek immediate medical attention if symptoms worsen or new symptoms develop
            - Regular follow-up with healthcare providers is essential
            - Maintain a symptom diary for better tracking
            - Follow all prescribed medications and treatments
            """
            
            return {
                'analysis': formatted_analysis,
                'symptoms_analyzed': symptoms,
                'patient_info_used': patient_info,
                'history_analysis': history_analysis,
                'recommendations': {
                    'diet': get_diet_recommendations(symptoms, patient_info),
                    'exercise': get_exercise_recommendations(symptoms, patient_info),
                    'stress': get_stress_management(symptoms, patient_info)
                }
            }
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(retry_delay)
                continue
            else:
                return generate_detailed_analysis(symptoms, patient_info)
    
    return generate_detailed_analysis(symptoms, patient_info)

def analyze_medical_history(history: str) -> Dict[str, str]:
    """Analyze medical history and provide detailed insights."""
    if not history or history.lower() == 'not provided':
        return {
            'summary': 'No medical history provided. Please provide medical history for better analysis.',
            'risk_factors': 'Unable to assess risk factors without medical history.',
            'complications': 'Unable to assess potential complications without medical history.',
            'recommended_tests': 'Standard screening tests recommended based on age and gender.',
            'precautions': 'General precautions recommended. Specific precautions require medical history.',
            'monitoring': 'Standard monitoring parameters recommended.'
        }
    
    # Analyze common medical conditions
    conditions = {
        'diabetes': ['diabetes', 'diabetic', 'blood sugar', 'insulin'],
        'hypertension': ['hypertension', 'high blood pressure', 'hbp'],
        'heart_disease': ['heart disease', 'cardiac', 'heart attack', 'angina'],
        'respiratory': ['asthma', 'copd', 'bronchitis', 'pneumonia'],
        'arthritis': ['arthritis', 'joint pain', 'rheumatoid', 'osteoarthritis'],
        'mental_health': ['depression', 'anxiety', 'bipolar', 'schizophrenia'],
        'allergies': ['allergies', 'allergic', 'anaphylaxis'],
        'cancer': ['cancer', 'tumor', 'malignancy', 'oncology']
    }
    
    detected_conditions = []
    for condition, keywords in conditions.items():
        if any(keyword in history.lower() for keyword in keywords):
            detected_conditions.append(condition)
    
    # Generate analysis based on detected conditions
    analysis = {
        'summary': generate_history_summary(detected_conditions),
        'risk_factors': generate_risk_factors(detected_conditions),
        'complications': generate_complications(detected_conditions),
        'recommended_tests': generate_recommended_tests(detected_conditions),
        'precautions': generate_precautions(detected_conditions),
        'monitoring': generate_monitoring_plan(detected_conditions)
    }
    
    return analysis

def generate_history_summary(conditions: List[str]) -> str:
    """Generate a summary of medical history analysis."""
    if not conditions:
        return "No specific medical conditions detected in the provided history."
    
    summary = "Detected medical conditions:\n"
    for condition in conditions:
        summary += f"- {condition.replace('_', ' ').title()}\n"
    return summary

def generate_risk_factors(conditions: List[str]) -> str:
    """Generate risk factors based on medical conditions."""
    if not conditions:
        return "Standard risk factors based on age and gender apply."
    
    risk_factors = "Additional risk factors based on medical history:\n"
    for condition in conditions:
        risk_factors += f"- {condition.replace('_', ' ').title()}-related complications\n"
    return risk_factors

def generate_complications(conditions: List[str]) -> str:
    """Generate potential complications based on medical conditions."""
    if not conditions:
        return "Standard complication monitoring recommended."
    
    complications = "Potential complications to monitor:\n"
    for condition in conditions:
        complications += f"- {condition.replace('_', ' ').title()}-related complications\n"
    return complications

def generate_recommended_tests(conditions: List[str]) -> str:
    """Generate recommended tests based on medical conditions."""
    if not conditions:
        return "Standard screening tests recommended."
    
    tests = "Additional tests recommended based on medical history:\n"
    for condition in conditions:
        tests += f"- {condition.replace('_', ' ').title()}-specific monitoring\n"
    return tests

def generate_precautions(conditions: List[str]) -> str:
    """Generate precautions based on medical conditions."""
    if not conditions:
        return "Standard precautions recommended."
    
    precautions = "Additional precautions based on medical history:\n"
    for condition in conditions:
        precautions += f"- {condition.replace('_', ' ').title()}-specific precautions\n"
    return precautions

def generate_monitoring_plan(conditions: List[str]) -> str:
    """Generate monitoring plan based on medical conditions."""
    if not conditions:
        return "Standard monitoring parameters recommended."
    
    monitoring = "Additional monitoring parameters based on medical history:\n"
    for condition in conditions:
        monitoring += f"- {condition.replace('_', ' ').title()}-specific monitoring\n"
    return monitoring

def get_diet_recommendations(symptoms: List[str], patient_info: Dict[str, Any]) -> str:
    """Get personalized diet recommendations."""
    return "Balanced diet with emphasis on whole foods, adequate hydration, and appropriate portion sizes"

def get_exercise_recommendations(symptoms: List[str], patient_info: Dict[str, Any]) -> str:
    """Get personalized exercise recommendations."""
    return "Regular moderate exercise as tolerated, with appropriate rest periods and gradual progression"

def get_stress_management(symptoms: List[str], patient_info: Dict[str, Any]) -> str:
    """Get stress management recommendations."""
    return "Regular relaxation techniques, adequate sleep, and stress-reduction activities"

def generate_detailed_analysis(symptoms: List[str], patient_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a detailed medical analysis when the AI model is unavailable."""
    return {
        'analysis': f"""
        Medical Analysis Report
        ======================
        
        Patient Information:
        -------------------
        Age: {patient_info.get('age', 'Not provided')}
        Gender: {patient_info.get('gender', 'Not provided')}
        Medical History: {patient_info.get('medical_history', 'Not provided')}
        
        Presenting Symptoms:
        ------------------
        {', '.join(symptoms)}
        
        Clinical Assessment:
        ------------------
        1. Differential Diagnosis:
           Based on the presenting symptoms, several conditions should be considered:
           - Acute conditions requiring immediate attention
           - Chronic conditions requiring ongoing management
           - Systemic conditions affecting multiple organ systems
        
        2. Risk Assessment:
           - Age-related factors: {get_age_risk_factors(patient_info.get('age'))}
           - Gender-specific considerations: {get_gender_considerations(patient_info.get('gender'))}
           - Lifestyle and medical history impact: {get_history_impact(patient_info.get('medical_history'))}
        
        3. Potential Complications:
           - Acute complications: {get_acute_complications(symptoms)}
           - Chronic implications: {get_chronic_implications(symptoms)}
        
        4. Recommended Diagnostic Workup:
           - Initial screening tests: {get_screening_tests(symptoms)}
           - Additional investigations: {get_additional_tests(symptoms)}
        
        5. Treatment Considerations:
           - Immediate interventions: {get_immediate_interventions(symptoms)}
           - Long-term management: {get_long_term_management(symptoms)}
        
        6. Follow-up Recommendations:
           - Monitoring parameters: {get_monitoring_parameters(symptoms)}
           - Referral criteria: {get_referral_criteria(symptoms)}
        
        Important Notes:
        --------------
        - This is an AI-generated preliminary analysis and should not replace professional medical evaluation
        - Seek immediate medical attention if symptoms worsen or new symptoms develop
        - Regular follow-up with healthcare providers is essential
        - Maintain a symptom diary for better tracking
        """,
        'symptoms_analyzed': symptoms,
        'patient_info_used': patient_info
    }

def get_age_risk_factors(age: str) -> str:
    """Get age-specific risk factors."""
    try:
        age_num = int(age)
        if age_num < 18:
            return "Pediatric considerations, developmental factors, growth monitoring"
        elif age_num < 65:
            return "Adult risk factors, lifestyle-related conditions, occupational health"
        else:
            return "Geriatric considerations, age-related conditions, polypharmacy risks"
    except:
        return "Age-specific risk factors cannot be determined"

def get_gender_considerations(gender: str) -> str:
    """Get gender-specific medical considerations."""
    gender = gender.lower()
    if gender == 'male':
        return "Male-specific conditions, hormonal factors, prostate health"
    elif gender == 'female':
        return "Female-specific conditions, hormonal factors, reproductive health"
    else:
        return "General health considerations"

def get_history_impact(history: str) -> str:
    """Analyze impact of medical history."""
    if not history or history.lower() == 'not provided':
        return "Medical history impact cannot be assessed"
    return "Consider impact of existing conditions on current symptoms"

def get_acute_complications(symptoms: List[str]) -> str:
    """Get potential acute complications based on symptoms."""
    return "Monitor for signs of deterioration, systemic involvement, and emergency conditions"

def get_chronic_implications(symptoms: List[str]) -> str:
    """Get potential chronic implications based on symptoms."""
    return "Consider long-term health impact, quality of life factors, and chronic disease management"

def get_screening_tests(symptoms: List[str]) -> str:
    """Get recommended initial screening tests."""
    return "Basic blood work, vital signs monitoring, and relevant imaging studies"

def get_additional_tests(symptoms: List[str]) -> str:
    """Get recommended additional diagnostic tests."""
    return "Specialized testing based on specific symptoms and risk factors"

def get_immediate_interventions(symptoms: List[str]) -> str:
    """Get recommended immediate interventions."""
    return "Supportive care, symptom management, and monitoring of vital signs"

def get_long_term_management(symptoms: List[str]) -> str:
    """Get recommended long-term management strategies."""
    return "Lifestyle modifications, preventive measures, and regular health monitoring"

def get_monitoring_parameters(symptoms: List[str]) -> str:
    """Get recommended monitoring parameters."""
    return "Vital signs, symptom progression, and response to interventions"

def get_referral_criteria(symptoms: List[str]) -> str:
    """Get criteria for specialist referral."""
    return "Refer to appropriate specialist if symptoms persist or worsen" 