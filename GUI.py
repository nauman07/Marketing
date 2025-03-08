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

# Define questions for each group
questions = {
    "Control Group": {
        "Page 1": [
            "Name",
            "Email",
            "Company",
            "Position",
            "Department"
        ],
        "Page 2": [
            "Based on the information provided, which supplier would you select for AeroConnect Airlines?",
            "Rate your confidence in this decision (1 = Not Confident at all, 10 = Extremely Confident)",
            "If you had to distribute AeroConnect’s annual orders across these suppliers, what % would you allocate to each? (Total % must equal 100)",
            "Supplier A: ____ %",
            "Supplier B: ____ %",
            "Supplier C: ____ %"
        ],
        "Page 3": [
            "I believe selecting a supplier with a lower reliability poses a risk to AeroConnect’s operations. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "I am concerned about potential hidden costs that might arise from selecting the lowest-price supplier. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "I would rather pay more upfront for avionics units than risk unexpected costs later. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "I am comfortable with longer and more variable lead times if it results in significant cost savings. (1 = Strongly Disagree, 5 = Strongly Agree)"
        ]
    },
    "Bias Group": {
        "Page 1": [
            "Name",
            "Email",
            "Company",
            "Position",
            "Department"
        ],
        "Page 2": [
            "Based on the information provided, which supplier would you select for AeroConnect Airlines?",
            "Rate your confidence in this decision, considering the potential impact on aircraft availability (1 = Not at all confident, 10 = Extremely confident)",
            "If you had to distribute AeroConnect's annual orders to manage supply risk, what percentage would you allocate to each supplier? (Total must equal 100%)",
            "Supplier A: ____%",
            "Supplier B: ____%",
            "Supplier C: ____%"
        ],
        "Page 3": [
            "Selecting a supplier with lower reliability exposes AeroConnect to significant operational disruptions, potential regulatory scrutiny, and passenger compensation claims. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "The hidden costs from selecting the lowest-price supplier (emergency shipments, flight cancellations, maintenance complications) often exceed the initial savings. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "Paying more upfront for quality avionics units protects against costly flight cancellations, emergency maintenance, and damage to AeroConnect's safety reputation. (1 = Strongly Disagree, 5 = Strongly Agree)",
            "Longer and variable lead times increase the risk of grounded aircraft and lost revenue when unexpected maintenance needs arise. (1 = Strongly Disagree, 5 = Strongly Agree)"
        ]
    }
}

# Supplier details
suppliers = {
    "Supplier A": {
        "Price": "$8,750/unit (25% above market average)",
        "Lead Time": "18 days (±4 days variability)",
        "Reliability": "97% defect-free rate",
        "Minimum Order Quantity": "15 units",
        "Additional": "FAA-certified manufacturing facility, 5-year warranty"
    },
    "Supplier B": {
        "Price": "$7,000/unit (Industry Benchmark)",
        "Lead Time": "20 days (±7 days variability)",
        "Reliability": "95% defect-free rate",
        "Minimum Order Quantity": "10 units",
        "Additional": "Recently ISO 9001 certified, 2-year warranty"
    },
    "Supplier C": {
        "Price": "$9,800/unit (40% above market average)",
        "Lead Time": "15 days (±2 days variability)",
        "Reliability": "99% defect-free rate",
        "Minimum Order Quantity": "20 units",
        "Additional": "Used by 7 of the top 10 global airlines, 7-year warranty"
    }
}

# Function to save responses to Firebase
def save_to_firebase(answers, is_control):
    try:
        user_name = answers.get("Name", "Unknown")
        collection_name = f"survey_{user_name.replace(' ', '_')}"
        processed_answers = {q: (answers.get(q, "N/A") or "N/A") for q in answers}
        processed_answers["is_control"] = is_control  # Add is_control field
        db.collection(collection_name).add(processed_answers)
        st.success("Data successfully saved to Firebase!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

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

# Function to display supplier details
def display_supplier_details():
    st.write("### Supplier Details")
    for supplier, details in suppliers.items():
        st.write(f"#### {supplier}")
        for key, value in details.items():
            st.write(f"- **{key}**: {value}")

# Function to display scenarios
def display_scenarios(is_control):
    st.write("### Scenario Description")
    if is_control:
        st.write("""
        **Control Group Scenario**:
        AeroConnect Airlines is reviewing its procurement strategy for avionics control units. The current supplier's contract is expiring, and the airline must select a new supplier. Each aircraft requires regular replacement of these units as part of scheduled maintenance procedures. The airline operates 45 commercial aircraft and plans to add 8 more within the next 18 months.
        """)
    else:
        st.write("""
        **Bias Group Scenario**:
        In the past year, airlines with supplier reliability issues reported operational disruptions averaging 3-5 days per incident. These disruptions resulted in maintenance costs, schedule adjustments, and customer compensation averaging $450,000 per incident. Quality control variations among suppliers were identified as the primary contributing factor. AeroConnect Airlines must select a new supplier for avionics control units, considering these risks.
        """)

# Main function for Control Group
def control_group():
    set_background("4689289055_06563de23c.irprodgera_tw8mx.jpeg")  # Replace with your image path
    display_header()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display scenarios and supplier details
    display_scenarios(is_control=True)
    display_supplier_details()

    # Get questions for the control group
    group_questions = questions["Control Group"]

    # Display questions based on the current page
    st.write(f"### {st.session_state.page}")
    for question in group_questions[st.session_state.page]:
        st.markdown(f"<p style='color: white; font-weight: 900;'>{question}</p>", unsafe_allow_html=True)
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a slider for rating questions
            st.session_state.answers[question] = st.slider("", 1, 10 if "confidence" in question else 5, key=question)
        else:
            # Use a text input for other questions
            st.session_state.answers[question] = st.text_input("", value=st.session_state.answers.get(question, ""), key=question)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    pages = list(group_questions.keys())
    current_index = pages.index(st.session_state.page)
    
    if current_index > 0 and col1.button("Previous"):
        st.session_state.page = pages[current_index - 1]
        st.rerun()
    
    if current_index < len(pages) - 1 and col3.button("Next"):
        st.session_state.page = pages[current_index + 1]
        st.rerun()
    
    # Submit button
    if st.session_state.page == "Page 3" and st.button("Submit"):
        save_to_firebase(st.session_state.answers, is_control=1)
        st.session_state.answers = {}
        st.session_state.page = "Page 1"  # Reset to first page after submission
        st.rerun()
    
    display_footer()

# Main function for Bias Group
def bias_group():
    set_background("rwth-aachen.jpg")  # Replace with your image path
    display_header()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display scenarios and supplier details
    display_scenarios(is_control=False)
    display_supplier_details()

    # Get questions for the bias group
    group_questions = questions["Bias Group"]

    # Display questions based on the current page
    st.write(f"### {st.session_state.page}")
    for question in group_questions[st.session_state.page]:
        st.markdown(f"<p style='color: white; font-weight: 900;'>{question}</p>", unsafe_allow_html=True)
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a slider for rating questions
            st.session_state.answers[question] = st.slider("", 1, 10 if "confidence" in question else 5, key=question)
        else:
            # Use a text input for other questions
            st.session_state.answers[question] = st.text_input("", value=st.session_state.answers.get(question, ""), key=question)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    pages = list(group_questions.keys())
    current_index = pages.index(st.session_state.page)
    
    if current_index > 0 and col1.button("Previous"):
        st.session_state.page = pages[current_index - 1]
        st.rerun()
    
    if current_index < len(pages) - 1 and col3.button("Next"):
        st.session_state.page = pages[current_index + 1]
        st.rerun()
    
    # Submit button
    if st.session_state.page == "Page 3" and st.button("Submit"):
        save_to_firebase(st.session_state.answers, is_control=0)
        st.session_state.answers = {}
        st.session_state.page = "Page 1"  # Reset to first page after submission
        st.rerun()
    
    display_footer()

# Main app routing
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Control Group", "Bias Group"])
    if app_mode == "Control Group":
        control_group()
    elif app_mode == "Bias Group":
        bias_group()

if __name__ == "__main__":
    main()
