import streamlit as st
from firebase_config import initialize_firebase
import base64
import pandas as pd

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

# Convert supplier data to a pandas DataFrame for tabular display
suppliers_df = pd.DataFrame(suppliers).transpose()
suppliers_df.index.name = "Supplier"
suppliers_df.reset_index(inplace=True)

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
            <h1>Group Survey</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to encode local image to Base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to display the footer with developer details
def display_footer():
    # Encode the local image to Base64
    image_path = "1705048040202.jpeg"  # Path to the local image
    image_base64 = get_image_base64(image_path)

    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-top: 20px;">
            <p>© 2025 RWTH Aachen University. All rights reserved.</p>
            <p>For more information or if you are facing any issues, please contact the developer:</p>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <img src="data:image/jpeg;base64,{image_base64}" alt="Developer Logo" width="50" style="border-radius: 50%;">
                <div>
                    <p style="margin: 0;"><strong>HarshVardhan Kanthode</strong></p>
                    <p style="margin: 0;">
                        <a href="mailto:harshvardhan.kanthode@rwth-aachen.de" style="text-decoration: none; color: inherit;">📧 Email</a> | 
                        <a href="https://www.linkedin.com/in/harshvardhan-kanthode-628863189/" target="_blank" style="text-decoration: none; color: inherit;">🔗 LinkedIn</a>
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_supplier_details():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: black;">Supplier Details</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Convert the DataFrame to HTML and inject custom CSS for the table
    table_html = suppliers_df.to_html(index=False, escape=False)
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: rgba(255, 255, 255, 0.8);
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                color: black; /* Ensure text color is black */
            }}
            th {{
                background-color: rgba(255, 255, 255, 0.8);
                color: black; /* Ensure header text color is black */
            }}
            </style>
            {table_html}
        </div>
        """,
        unsafe_allow_html=True
    )
    
def display_scenario():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: black;">Scenario Description</h3>
            <p style="color: black;">
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

# Function to display numeric input with semi-transparent background
def display_numeric_input(question, min_value, max_value, key):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    value = st.number_input("", min_value=min_value, max_value=max_value, value=min_value, key=key)
    return value

# Main function for Control Group
def control_group():
    set_background("rwth-aachen.jpg")  # Background image
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
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a numeric input for rating questions
            min_value = 1
            max_value = 10 if "confidence" in question else 5
            st.session_state.answers[question] = display_numeric_input(question, min_value, max_value, key=question)
        else:
            # Use a text input for other questions
            display_question(question)
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
