import streamlit as st
from model import DiseasePredictor
from data import SYMPTOMS, get_severity_mapping, get_gender_mapping
from datetime import datetime

def initialize_session_state():
    if 'predictor' not in st.session_state:
        st.session_state.predictor = DiseasePredictor()

def display_recommendations(recommendations):
    if recommendations:
        st.subheader("Ayurvedic Recommendations")

        # Display herbs
        st.write("🌿 **Recommended Herbs:**")
        for herb in recommendations['herbs']:
            st.write(f"- {herb}")

        # Display lifestyle recommendations
        st.write("🧘‍♀️ **Lifestyle Recommendations:**")
        for lifestyle in recommendations['lifestyle']:
            st.write(f"- {lifestyle}")

        # Display diet recommendations
        st.write("🥗 **Diet Recommendations:**")
        for diet in recommendations['diet']:
            st.write(f"- {diet}")

def generate_report(age, gender, selected_symptoms, severity, predicted_disease, confidence, recommendations):
    """Generate a detailed health report"""
    report = []

    # Header
    report.append("# Ayurvedic Health Assessment Report")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Patient Information
    report.append("## Patient Information")
    report.append(f"- **Age:** {age} years")
    report.append(f"- **Gender:** {get_gender_mapping()[gender]}")
    report.append(f"- **Severity Level:** {get_severity_mapping()[severity]}\n")

    # Symptoms
    report.append("## Reported Symptoms")
    for symptom in selected_symptoms:
        report.append(f"- {symptom}")
    report.append("")

    # Prediction Results
    report.append("## Disease Prediction")
    report.append(f"- **Predicted Condition:** {predicted_disease}")
    report.append(f"- **Confidence Score:** {confidence:.2%}\n")

    # Recommendations
    report.append("## Ayurvedic Recommendations")

    # Herbs
    report.append("### Recommended Herbs")
    for herb in recommendations['herbs']:
        report.append(f"- {herb}")
    report.append("")

    # Lifestyle
    report.append("### Lifestyle Recommendations")
    for lifestyle in recommendations['lifestyle']:
        report.append(f"- {lifestyle}")
    report.append("")

    # Diet
    report.append("### Dietary Guidelines")
    for diet in recommendations['diet']:
        report.append(f"- {diet}")
    report.append("")

    # Disclaimer
    report.append("## Disclaimer")
    report.append("⚠️ This is a preliminary assessment system. Please consult with a qualified Ayurvedic practitioner for proper diagnosis and treatment.")

    return "\n".join(report)

def main():
    initialize_session_state()

    st.title("Ayurvedic Disease Prediction System")
    st.write("Enter your symptoms and details for disease prediction and Ayurvedic recommendations")

    with st.form("prediction_form"):
        # Symptoms selection
        selected_symptoms = st.multiselect(
            "Select your symptoms",
            options=SYMPTOMS,
            help="Choose all applicable symptoms"
        )

        # Age input
        age = st.number_input(
            "Enter your age",
            min_value=0,
            max_value=120,
            value=30,
            help="Age in years"
        )

        # Severity selection
        severity = st.select_slider(
            "Select severity of symptoms",
            options=[1, 2, 3],
            value=1,
            format_func=lambda x: get_severity_mapping()[x],
            help="1: Mild, 2: Moderate, 3: Severe"
        )

        # Gender selection
        gender = st.selectbox(
            "Select your gender",
            options=["M", "F"],
            format_func=lambda x: get_gender_mapping()[x],
            help="Select your gender"
        )

        submitted = st.form_submit_button("Predict Disease")

    if submitted:
        if not selected_symptoms:
            st.error("Please select at least one symptom")
            return

        with st.spinner("Analyzing symptoms..."):
            # Get prediction
            predicted_disease, confidence = st.session_state.predictor.predict(
                selected_symptoms, age, severity, gender
            )

            # Get recommendations
            recommendations = st.session_state.predictor.get_recommendations(
                predicted_disease, age, gender, severity
            )

            # Display results
            st.success("Analysis Complete!")

            # Generate and display report
            report = generate_report(
                age=age,
                gender=gender,
                selected_symptoms=selected_symptoms,
                severity=severity,
                predicted_disease=predicted_disease,
                confidence=confidence,
                recommendations=recommendations
            )

            # Display the report in the UI
            st.markdown(report)

if __name__ == "__main__":
    main()