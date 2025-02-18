import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/admin/Downloads/marketingquestionnaire-edfa9-firebase-adminsdk-fbsvc-5776b409ec.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Define questions
questions = [
    "Name",
    "Email",
    "Company",
    "Position",
    "Department",
    "What is your favorite color?",
    "How many hours do you work daily?",
    "Do you prefer tea or coffee?",
    "What is your favorite hobby?"
]

def store_answers(answers):
    doc_id = str(uuid.uuid4())  # Unique ID for each response
    db.collection("responses").document(doc_id).set(answers)

def main():
    st.title("User Questionnaire")
    
    st.write("Please answer the following questions:")
    
    user_answers = {}
    for question in questions:
        answer = st.text_input(question, "")
        user_answers[question] = answer
    
    if st.button("Submit"):
        store_answers(user_answers)
        st.success("Thank you! Your responses have been recorded.")

if __name__ == "__main__":
    main()
