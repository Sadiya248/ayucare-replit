import pandas as pd
import numpy as np

def load_datasets():
    # Load and process the drug dataset
    drug_data = pd.read_csv('attached_assets/Drug prescription Dataset (1).csv')
    
    # Create symptoms dataset from the drug data columns
    symptoms = ['acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision', 
               'excessive_hunger', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
               'movement_stiffness', 'depression', 'irritability', 'visual_disturbances',
               'painful_walking', 'abdominal_pain', 'nausea', 'vomiting', 'blood_in_mucus',
               'Fatigue', 'Fever', 'Dehydration', 'loss_of_appetite', 'cramping']
               
    # Create a symptoms dataset with binary values
    symptoms_data = pd.DataFrame(columns=symptoms + ['prognosis'])
    unique_diseases = drug_data['disease'].unique()
    
    # Create symptom patterns for each disease
    for disease in unique_diseases:
        symptom_row = pd.Series(0, index=symptoms + ['prognosis'])
        disease_symptoms = drug_data[drug_data['disease'] == disease].iloc[0]
        
        # Set relevant symptoms to 1
        for symptom in symptoms:
            if disease_symptoms.get(symptom, 0) == 1:
                symptom_row[symptom] = 1
        
        symptom_row['prognosis'] = disease
        symptoms_data = pd.concat([symptoms_data, symptom_row.to_frame().T], ignore_index=True)
    
    return symptoms_data, drug_data

def get_symptoms():
    symptoms_data, _ = load_datasets()
    # Exclude the last 'prognosis' column
    symptom_columns = symptoms_data.columns[:-1]  
    return list(symptom_columns)

def get_diseases():
    symptoms_data, _ = load_datasets()
    return list(symptoms_data['prognosis'].unique())

def get_severity_mapping():
    return {1: "LOW", 2: "NORMAL", 3: "HIGH"}

def get_gender_mapping():
    return {"M": "male", "F": "female"}

# Global variables
SYMPTOMS = get_symptoms()
DISEASES = get_diseases()

def get_drug_recommendations(disease, age, gender, severity):
    """Get Ayurvedic recommendations for the predicted disease"""
    _, drug_data = load_datasets()

    # Convert severity to string format used in dataset
    severity_map = {1: "LOW", 2: "NORMAL", 3: "HIGH"}
    severity_str = severity_map[severity]

    # Convert gender to format used in dataset
    gender_map = {"M": "male", "F": "female", "O": "other"}
    gender_str = gender_map[gender]

    # Filter recommendations - more flexible matching
    matching_drugs = drug_data[
        (drug_data['disease'].str.lower().str.contains(disease.lower())) &
        (drug_data['gender'] == gender_str)]

    # Get the closest age match
    if not matching_drugs.empty:
        matching_drugs['age_diff'] = abs(matching_drugs['age'] - age)
        closest_match = matching_drugs.loc[matching_drugs['age_diff'].idxmin()]

        return {
            'herbs': [closest_match['drug']],
            'lifestyle': ["Regular exercise", "Proper rest", "Balanced diet"],
            'diet': [
                "Avoid triggering foods",
                "Stay hydrated",
                "Eat fresh fruits and vegetables"
            ]
        }

    # Fallback recommendations if no match found
    return {
        'herbs': ["General Ayurvedic herbs"],
        'lifestyle': ["Regular exercise", "Proper rest", "Balanced diet"],
        'diet': [
            "Avoid triggering foods",
            "Stay hydrated", 
            "Eat fresh fruits and vegetables"
        ]
    }