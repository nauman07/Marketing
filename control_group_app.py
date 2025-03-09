import streamlit as st
from firebase_config import initialize_firebase
import base64

# Initialize Firebase
db = initialize_firebase()

# Questions for Control Group
questions = {
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
        "Supplier A: in %",
        "Supplier B: in %",
        "Supplier C: in %"
    ],
    "Page 3": [
        "I believe selecting a supplier with a lower reliability poses a risk to AeroConnect’s operations. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "I am concerned about potential hidden costs that might arise from selecting the lowest-price supplier. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "I would rather pay more upfront for avionics units than risk unexpected costs later. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "I am comfortable with longer and more variable lead times if it results in significant cost savings. (1 = Strongly Disagree, 5 = Strongly Agree)"
    ]
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
def save_to_firebase(answers):
    try:
        user_name = answers.get("Name", "Unknown")
        collection_name = f"survey_{user_name.replace(' ', '_')}"
        processed_answers = {q: (answers.get(q, "N/A") or "N/A") for q in answers}
        processed_answers["is_control"] = True  # Mark as Control Group
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
        <div style="text-align: center; padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px;">
            <img src="https://www.total-e-quality.de/media/cache/71/47/71471181693ed2ace2081f0e9adf4df9.png" width="100">
            <h1>Control Group Survey</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display the footer
def display_footer():
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-top: 20px;">
            <p>© 2023 RWTH Aachen University. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display supplier details
def display_supplier_details():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <h3>Supplier Details</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    for supplier, details in suppliers.items():
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
                <h4>{supplier}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        for key, value in details.items():
            st.markdown(
                f"""
                <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
                    <p><strong>{key}</strong>: {value}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# Function to display scenarios
def display_scenario():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <h3>Scenario Description</h3>
            <p>
                <strong>Group Scenario:</strong><br>
                AeroConnect Airlines is reviewing its procurement strategy for avionics control units. The current supplier's contract is expiring, and the airline must select a new supplier. Each aircraft requires regular replacement of these units as part of scheduled maintenance procedures. The airline operates 45 commercial aircraft and plans to add 8 more within the next 18 months.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display questions with semi-transparent background
def display_question(question):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display slider with semi-transparent background
def display_slider(question, min_value, max_value, key):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    return st.slider("", min_value, max_value, key=key)

# Main function for Control Group
def control_group():
    set_background("krantz-acs-rwth-carl-aachen-referenz-galerie-01.webp")  # Background image
    display_header()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display scenario and supplier details
    display_scenario()
    display_supplier_details()

    # Display questions based on the current page
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <h3>{st.session_state.page}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    for question in questions[st.session_state.page]:
        display_question(question)
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a slider for rating questions
            st.session_state.answers[question] = display_slider(question, 1, 10 if "confidence" in question else 5, key=question)
        else:
            # Use a text input for other questions
            st.session_state.answers[question] = st.text_input("", value=st.session_state.answers.get(question, ""), key=question)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    pages = list(questions.keys())
    current_index = pages.index(st.session_state.page)
    
    if current_index > 0 and col1.button("Previous"):
        st.session_state.page = pages[current_index - 1]
        st.rerun()
    
    if current_index < len(pages) - 1 and col3.button("Next"):
        st.session_state.page = pages[current_index + 1]
        st.rerun()
    
    # Submit button
    if st.session_state.page == "Page 3" and st.button("Submit"):
        save_to_firebase(st.session_state.answers)
        st.session_state.answers = {}
        st.session_state.page = "Page 1"  # Reset to first page after submission
        st.rerun()
    
    display_footer()
    
if __name__ == "__main__":
    control_group()
