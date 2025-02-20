import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64
import os
from PIL import Image

# Initialize Firebase using Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(st.secrets["firebase_credentials"]))
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
    db.collection("survey_responses").add(answers)

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
        st.session_state.answers[question] = st.text_input(question, value=st.session_state.answers.get(question, ""))

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    if st.session_state.page != "Page 1" and col1.button("Previous"):
        st.session_state.page = "Page 1" if st.session_state.page == "Page 2" else "Page 2"
    if st.session_state.page != "Page 3" and col3.button("Next"):
        st.session_state.page = "Page 2" if st.session_state.page == "Page 1" else "Page 3"
    
    # Submit button
    if st.session_state.page == "Page 3" and st.button("Submit"):
        save_to_firebase(st.session_state.answers)
        st.success("Thank you! Your responses have been recorded.")
        st.session_state.answers = {}
    
    display_footer()

if __name__ == "__main__":
    main()
