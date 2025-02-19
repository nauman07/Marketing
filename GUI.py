import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image

# Define the CSV file to store data
data_file = "data.csv"

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

# Function to save responses to CSV
def save_to_csv(answers):
    if os.path.exists(data_file):
        df = pd.read_csv(data_file, index_col=["Name", "Email"])
    else:
        df = pd.DataFrame(columns=["Name", "Email"] + list(questions["Page 2"]) + list(questions["Page 3"]))
    
    new_entry = pd.DataFrame([answers]).set_index(["Name", "Email"])
    df = pd.concat([df, new_entry])
    df.to_csv(data_file)

# Function to set a background image with animation
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
            animation: moveBackground 20s linear infinite;
        }}
        @keyframes moveBackground {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to display the header with a logo
def display_header():
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/RWTH_Aachen_University_Logo.svg/1200px-RWTH_Aachen_University_Logo.svg.png" alt="Logo" width="100">
            <h1>New Survey</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display the footer
def display_footer():
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 10px; margin-top: 20px;">
            <p>© 2023 RWTH Aachen University. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main function
def main():
    # Set background animation
    set_background("rwth-aachen.jpg")  # Replace with your image path

    # Display header
    display_header()

    # Initialize session state for page navigation and answers
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display questions based on the current page
    st.write(f"### {st.session_state.page}")
    for question in questions[st.session_state.page]:
        #st.markdown(f"<p style='font-weight: bold;'>{question}</p>", unsafe_allow_html=True)
        st.session_state.answers[question] = st.text_input(question, value=st.session_state.answers.get(question, ""), key=question)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    if st.session_state.page != "Page 1":
        if col1.button("Previous"):
            if st.session_state.page == "Page 2":
                st.session_state.page = "Page 1"
            elif st.session_state.page == "Page 3":
                st.session_state.page = "Page 2"

    if st.session_state.page != "Page 3":
        if col3.button("Next"):
            if st.session_state.page == "Page 1":
                st.session_state.page = "Page 2"
            elif st.session_state.page == "Page 2":
                st.session_state.page = "Page 3"

    # Submit button (only on the last page)
    if st.session_state.page == "Page 3":
        if st.button("Submit"):
            save_to_csv(st.session_state.answers)
            st.success("Thank you! Your responses have been recorded.")
            st.session_state.answers = {}  # Clear answers after submission

    # Display footer
    display_footer()

if __name__ == "__main__":
    main()
