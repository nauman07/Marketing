import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64
import os
from PIL import Image

# Initialize Firebase using Streamlit secrets
firebase_credentials = {
    "type": st.secrets["firebase_credentials"]["type"],
    "project_id": st.secrets["firebase_credentials"]["project_id"],
    "private_key_id": st.secrets["firebase_credentials"]["private_key_id"],
    "private_key": st.secrets["firebase_credentials"]["private_key"].replace("\\n", "\n"),  # Fix private key formatting
    "client_email": st.secrets["firebase_credentials"]["client_email"],
    "client_id": st.secrets["firebase_credentials"]["client_id"],
    "auth_uri": st.secrets["firebase_credentials"]["auth_uri"],
    "token_uri": st.secrets["firebase_credentials"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase_credentials"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase_credentials"]["client_x509_cert_url"]
}
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Define questions for each page
questions = {
    "Page 1": [
        "Name",
        "Email",
        "Company",
        "Position",
        "Department"
    ],
    "Page 2": [
        "What is your favorite color?",
        "How many hours do you work daily?",
        "Do you prefer tea or coffee?"
    ],
    "Page 3": [
        "What is your favorite hobby?",
        "What is your favorite book?",
        "What is your favorite movie?"
    ]
}

# Function to save responses to Firebase
def save_to_firebase(answers):
    try:
        processed_answers = {q: (answers.get(q, "N/A") or "N/A") for q in answers}
        db.collection("survey_responses").add(processed_answers)
        st.success("Data successfully saved to Firebase!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Function to insert dummy data for testing Firebase connectivity
def insert_dummy_data():
    try:
        dummy_data = {
            "Name": "John Doe",
            "Email": "john.doe@example.com",
            "Company": "TestCorp",
            "Position": "Engineer",
            "Department": "IT",
            "Favorite Color": "Blue",
            "Work Hours": "8",
            "Tea or Coffee": "Coffee",
            "Hobby": "Reading",
            "Book": "1984",
            "Movie": "Inception"
        }
        db.collection("survey_responses").add(dummy_data)
        st.success("Dummy data added successfully!")
    except Exception as e:
        st.error(f"Error adding dummy data: {e}")

# Function to test Firebase connectivity
def test_firebase_connection():
    try:
        docs = db.collection("survey_responses").limit(1).stream()
        for _ in docs:
            st.success("Successfully connected to Firebase!")
            return
        st.warning("Connected to Firebase, but no data found.")
    except Exception as e:
        st.error(f"Firebase connection failed: {e}")

# Function to set a background image
def set_background(image_path):
    with open(image_path, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to display the header with a logo
def display_header():
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://www.total-e-quality.de/media/cache/71/47/71471181693ed2ace2081f0e9adf4df9.png" width="100">
            <h1>New Survey</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display the footer
def display_footer():
    st.markdown(
        """
        <div style="text-align: center; background-color: #f0f0f0; padding: 10px; margin-top: 20px;">
            <p>© 2023 RWTH Aachen University. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main function
def main():
    set_background("4689289055_06563de23c.irprodgera_tw8mx.jpeg")  # Replace with your image path
    display_header()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display questions based on the current page
    st.write(f"### {st.session_state.page}")
    for question in questions[st.session_state.page]:
        st.markdown(f"<p style='color: black; font-weight: bold;'>{question}</p>", unsafe_allow_html=True)
        st.session_state.answers[question] = st.text_input("", value=st.session_state.answers.get(question, ""), key=question)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    pages = list(questions.keys())
    current_index = pages.index(st.session_state.page)
    
    if current_index > 0 and col1.button("Previous"):
        st.session_state.page = pages[current_index - 1]
    
    if current_index < len(pages) - 1 and col3.button("Next"):
        st.session_state.page = pages[current_index + 1]
    
    # Submit button
    if st.session_state.page == "Page 3" and st.button("Submit"):
        save_to_firebase(st.session_state.answers)
        st.session_state.answers = {}
        st.session_state.page = "Page 1"  # Reset to first page after submission
    
    # Buttons for testing Firebase connectivity
    if st.button("Insert Dummy Data"):
        insert_dummy_data()
    if st.button("Test Firebase Connection"):
        test_firebase_connection()
    
    display_footer()

if __name__ == "__main__":
    main()
