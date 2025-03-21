import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from data import load_datasets, SYMPTOMS, get_drug_recommendations

class DiseasePredictor:
    def __init__(self):
        # Load and prepare data
        self.symptoms = SYMPTOMS
        symptoms_data, _ = load_datasets()

        # Prepare features and target
        X = symptoms_data[self.symptoms].values
        y = symptoms_data['prognosis'].values

        # Split data into train, validation and test sets (60-20-20)
        from sklearn.model_selection import train_test_split

        # Use smaller training set: 50% train, 25% val, 25% test
        X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.33, random_state=42)

        # Use simpler model with more constraints
        self.model = DecisionTreeClassifier(
            max_depth=3,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42
        )
        self.model.fit(X_train, y_train)

        # Validate model
        val_score = self.model.score(X_val, y_val)
        test_score = self.model.score(X_test, y_test)
        print(f"Validation accuracy: {val_score:.2f}")
        print(f"Test accuracy: {test_score:.2f}")

    def preprocess_input(self, selected_symptoms):
        # Create feature vector
        feature_vector = np.zeros(len(self.symptoms))
        for symptom in selected_symptoms:
            if symptom in self.symptoms:
                idx = self.symptoms.index(symptom)
                feature_vector[idx] = 1
        # Scale the features
        return feature_vector.reshape(1, -1) # Removed scaling as it's not needed for Decision Tree

    def predict(self, selected_symptoms, age, severity, gender):
        """
        Predict disease based on symptoms and get confidence score with added uncertainty
        """
        # Preprocess input
        features = self.preprocess_input(selected_symptoms)

        # Get prediction and probability
        predicted_disease = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Get confidence based on symptom count and probability
        symptom_count = len(selected_symptoms)
        min_symptoms = 3
        
        if symptom_count < min_symptoms:
            confidence = 0.3  # Low confidence if too few symptoms
        else:
            # Find probability for predicted class
            class_idx = list(self.model.classes_).index(predicted_disease)
            base_confidence = probabilities[class_idx]
            
            # Adjust based on symptom count
            symptom_weight = min(1.0, symptom_count / 7)  # Max weight at 7 symptoms
            confidence = base_confidence * symptom_weight

        return predicted_disease, min(confidence, 0.95)  # Cap at 95%

    def get_recommendations(self, disease, age=30, gender='M', severity=2):
        """Get Ayurvedic recommendations for the predicted disease"""
        return get_drug_recommendations(disease, age, gender, severity)