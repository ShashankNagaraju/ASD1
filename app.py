import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load('autism_model.pkl')

# Ethnicity Mapping
ethnicity_options = {
    "Hispanic": 0, "Latino": 1, "Native Indian": 2, "Others": 3, "Pacifica": 4,
    "White European": 5, "Asian": 6, "Black": 7, "Middle Eastern": 8,
    "Mixed": 9, "South Asian": 10
}

# Response Mapping
response_mapping = {"Always": 1, "Usually": 1, "Sometimes": 1, "Rarely": 0, "Never": 0}

# Gender Mapping
gender_mapping = {"Male": 1, "Female": 0, "Other": 2}

# CSS Styling
# CSS Styling with Light Background
st.markdown("""
    <style>
    .stApp {background: linear-gradient(to right, #ffffff, #f8f9fa);}
    .title {font-size: 45px; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 30px;}
    .question-box {background: #f9f9f9; padding: 25px; border-radius: 12px;
                   box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.1); margin-bottom: 30px;}
    .question-text {font-size: 24px; font-weight: bold; color: #2d3436; margin-bottom: 15px;}
    .option-label {font-size: 22px; font-weight: bold; color: #636e72; padding: 10px;}
    .next-btn {background-color: #0984e3; color: white; font-size: 22px; padding: 12px 24px;
               border-radius: 8px; cursor: pointer; width: 100%; text-align: center;}
    .result-box {background: #dfe6e9; padding: 30px; border-radius: 15px;
                 box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2); text-align: center; font-size: 26px;
                 font-weight: bold; color: #2d3436;}
    </style>
""", unsafe_allow_html=True)


# Header
st.markdown('<h1 class="title">🔍 ASD Traits Prediction</h1>', unsafe_allow_html=True)

# 10 Behavioral Questions
questions = [
    "Does your child avoid eye contact?",
    "Does your child prefer to play alone?",
    "Does your child have difficulty understanding emotions?",
    "Does your child engage in repetitive movements or behaviors?",
    "Does your child resist changes in routine?",
    "Does your child have delayed speech development?",
    "Does your child have unusual sensory responses?",
    "Does your child exhibit limited interests?",
    "Does your child have difficulty making friends?",
    "Does your child frequently get upset without a clear reason?"
]

# 5 Additional Features
additional_features = {
    "Sex": list(gender_mapping.keys()),
    "Ethnicity": list(ethnicity_options.keys()),
    "Age (in months)": [str(i) for i in range(1, 229)],  # 1 month to 228 months (19 years)
    "Jaundice": ["Yes", "No"],
    "Family ASD History": ["Yes", "No"]
}

# Session State Initialization
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'additional_responses' not in st.session_state:
    st.session_state.additional_responses = {}

# Display Behavioral Questions First
if st.session_state.question_index < len(questions):
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">Q{st.session_state.question_index + 1}: {questions[st.session_state.question_index]}</div>', unsafe_allow_html=True)

    response = st.radio(
        "Select an option:",
        list(response_mapping.keys()),
        index=None,
        key=f"q_{st.session_state.question_index}",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Submit & Next"):
        if response is not None:
            st.session_state.responses.append(response_mapping[response])
            st.session_state.question_index += 1
            st.experimental_rerun()
        else:
            st.warning("Please select an option before proceeding.")

# After Behavioral Questions, Ask Additional Features
elif st.session_state.question_index == len(questions):
    st.markdown("---")
    st.markdown('<h2 style="text-align: center; color:#f4d03f;">Additional Information</h2>', unsafe_allow_html=True)

    for feature, options in additional_features.items():
        if feature not in st.session_state.additional_responses:
            st.session_state.additional_responses[feature] = None

        st.session_state.additional_responses[feature] = st.selectbox(
            feature, options, index=None, key=f"feature_{feature}"
        )

    if st.button("Submit & Predict"):
        if None not in st.session_state.additional_responses.values():
            st.session_state.question_index += 1
            st.experimental_rerun()
        else:
            st.warning("Please fill in all additional details before proceeding.")

# Show Results After Collecting All Features
elif st.session_state.question_index == len(questions) + 1:
    st.markdown("---")
    st.markdown('<div class="question-box"><h2 style="text-align: center; color:#f4d03f;">Processing Results...</h2></div>', unsafe_allow_html=True)

    # Prepare Input Data (10 responses + 5 additional features)
    input_data = np.array(
        st.session_state.responses + [
            gender_mapping[st.session_state.additional_responses["Sex"]],
            ethnicity_options[st.session_state.additional_responses["Ethnicity"]],
            int(st.session_state.additional_responses["Age (in months)"]),
            1 if st.session_state.additional_responses["Jaundice"] == "Yes" else 0,
            1 if st.session_state.additional_responses["Family ASD History"] == "Yes" else 0
        ]
    ).reshape(1, -1)

    # Prediction
    prediction = model.predict(input_data)[0]
    result = "🛑 **ASD Traits Detected**" if prediction == 1 else "✅ **No ASD Traits**"

    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    # Restart Quiz
    if st.button("Restart Quiz"):
        st.session_state.question_index = 0
        st.session_state.responses = []
        st.session_state.additional_responses = {}
        st.experimental_rerun()
