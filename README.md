ASD Traits Prediction
This is a Streamlit-based web application that predicts Autism Spectrum Disorder (ASD) traits based on user responses to behavioral questions and additional demographic information.

🚀 Getting Started
1️⃣ Install Dependencies
First, make sure you have Python installed, then install the required libraries: pip install streamlit joblib numpy
2️⃣ Run the Application
streamlit run app.py
This will launch the web application in your browser.

🌐 Live Demo
You can try the deployed version here:
🔗 ASD Companion

🛠 Features
Interactive Questionnaire: Users answer behavioral questions related to ASD symptoms.
Additional Information Input: Users provide gender, ethnicity, age, jaundice history, and ASD family history.
Machine Learning Model: A pre-trained model (autism_model.pkl) predicts ASD traits.
Responsive UI with Dark Theme: The interface adapts for better user experience.

📌 Notes
Ensure autism_model.pkl is in the same directory as app.py.
Modify requirements.txt if additional dependencies are needed.

📖 Learn More
Streamlit Documentation
Joblib for Model Persistence
