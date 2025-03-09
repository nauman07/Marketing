import streamlit as st
from firebase_config import initialize_firebase
import base64
import pandas as pd

# Initialize Firebase
db = initialize_firebase()

# Questions for Bias Group
questions = {
    "Page 1": [
        "First Name (Mandatory)",
        "Last Name",
        "Email",
        "Company",
        "Position",
        "Department"
    ],
    "Page 2": [
        "Based on the information provided, which supplier would you select for AeroConnect Airlines?",
        "Rate your confidence in this decision, considering the potential impact on aircraft availability (1 = Not at all confident, 10 = Extremely confident)",
        "If you had to distribute AeroConnect's annual orders to manage supply risk, what percentage would you allocate to each supplier? (Total must equal 100%)",
        "Supplier A: in %",
        "Supplier B: in %",
        "Supplier C: in %"
    ],
    "Page 3": [
        "Selecting a supplier with lower reliability exposes AeroConnect to significant operational disruptions, potential regulatory scrutiny, and passenger compensation claims. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "The hidden costs from selecting the lowest-price supplier (emergency shipments, flight cancellations, maintenance complications) often exceed the initial savings. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "Paying more upfront for quality avionics units protects against costly flight cancellations, emergency maintenance, and damage to AeroConnect's safety reputation. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "Longer and variable lead times increase the risk of grounded aircraft and lost revenue when unexpected maintenance needs arise. (1 = Strongly Disagree, 5 = Strongly Agree)"
    ],
    "Page 4: Follow-up Scenarios": [
        "If Supplier B improved their reliability rating to 97% but increased their price by 10%, would you change your original supplier selection? (Note- Each 1% decrease in reliability has historically corresponded to a 15% increase in maintenance issues)",
        "What is the minimum reliability percentage you would consider acceptable? (Each reliability percentage point below 99% correlates with approximately 3 additional flight cancellations per year)",
        "If a delivery delay grounds aircraft and disrupts operations, which option would you prefer?"
    ],
    "Page 5: Importance Ratings": [
        "Rate the importance of each factor in your supplier selection decision: (1 = Not Important, 2 = Slightly Important, 3 = Moderately Important, 4 = Very Important, 5 = Extremely Important)",
        "Which attribute would you be most willing to compromise on to improve reliability by 2%?"
    ],
    "Page 6: Long-term Considerations": [
        "Would you be willing to commit to a 2-year contract with your chosen supplier in exchange for a 12% price reduction? (Note- This would protect against any potential future price increases due to market volatility)",
        "How much would you be willing to invest in additional quality testing equipment that could detect potential defects before installation?"
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
        user_name = answers.get("First Name (Mandatory)", "Unknown")
        collection_name = f"survey_{user_name.replace(' ', '_')}"
        processed_answers = {q: (answers.get(q, "N/A") or "N/A") for q in answers}
        processed_answers["is_control"] = False  # Mark as Bias Group
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
        <div style="text-align: center; padding: 10px;">
            <img src="https://www.total-e-quality.de/media/cache/71/47/71471181693ed2ace2081f0e9adf4df9.png" width="100">
            <h1>Survey: Supplier Selection for Aircraft CDU</h1>
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
        <div style="text-align: center; padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-top: 20px;">
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

# Function to display supplier details in a table with semi-transparent background
def display_supplier_details():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: black;">Evaluation Criteria</h3>
            <p style="color: black;">
                You are expected to evaluate the suppliers through various criteria: <strong>Lead Time, Lead Variability, Reliability, Price, Minimum Order Quantity, Certification Standards, and Warranty Period</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: black;">Supplier Details</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Convert the DataFrame to HTML and inject custom CSS for the table
    table_html = suppliers_df.to_html(index=False, escape=False)
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: rgba(255, 255, 255);
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                color: black; /* Ensure text color is black */
            }}
            th {{
                background-color: rgba(255, 255, 255);
                color: black; /* Ensure header text color is black */
            }}
            </style>
            {table_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display scenarios
def display_scenario():
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: black;">Scenario Description</h3>
            <p style="color: black;">
                <strong> Case Study Background:</strong><br>
                AeroConnect Airlines has been rapidly expanding its fleet and network over the past three years. As part of its operational optimization initiative, the airline is reviewing its procurement strategy for critical aircraft components. Your team has been tasked with selecting a new supplier for <strong>Avionics Control Units</strong>, which are essential components that manage flight-critical electronic systems throughout the aircraft. This survey aims to evaluate your selection criteria for 3 suppliers for the CDU Component.
            </p>
            <p style="color: black;">
                <strong>Component Overview: Control Display Unit (CDU)</strong><br>
                CDUs are essential components in modern aircrafts, enabling pilots to manage and monitor various flight systems. The <strong>Control Display Unit (CDU)</strong> serves as the primary interface for pilots to interact with the aircraft's avionics systems. The CDU allows for flight management, system monitoring, and operational control, making it indispensable for safe and efficient flight operations.
            </p>
            <p style="color: black;">
                <strong>Key Applications of the CDU:</strong><br>
                - <strong>Flight Management:</strong> Input navigation waypoints, flight plans, and performance data.<br>
                - <strong>Communication:</strong>Communicate information to other avionics systems like the Flight Management System (FMS), Autopilot, and Navigation Display.<br>
                - <strong>Fuel Management:</strong> Manage the aircraft fuel system and optimize fuel efficiency to ensure sufficient reserves for the duration of the flight.<br>
                - <strong>System Diagnostics:</strong> Monitor performance parameters and diagnose abnormalities.
            </p>
            <p style="color: black;">
                <strong>Problem Statement:</strong><br>
                The current supplier's contract is expiring in <strong>60 days</strong>, and the procurement department must finalize a new supplier relationship. AeroConnect operates <strong>45 commercial aircraft</strong> with plans to add <strong>8 more within the next 18 months</strong>. Each aircraft requires regular replacement of these units as part of scheduled maintenance procedures.
            </p>
            <p style="color: black;">
                The Avionics Control Units are critical safety components - any malfunction could potentially lead to flight delays, cancellations, or in extreme cases, safety incidents requiring investigation. The airline's maintenance schedule indicates it will need approximately <strong>120 units annually</strong>.
            </p>
            <p style="color: black;">
                <strong>Your Task:</strong><br>
                As the procurement specialist, you must evaluate <strong>3</strong> potential suppliers and make a recommendation. Your decision will impact not only cost structures but also maintenance schedules, parts availability, and potentially operational reliability.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="padding: 10px; background-color: rgba(255, 0, 0); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: white;">
                <strong>Industry Data:</strong><br>
                In the past year, airlines with supplier reliability issues reported operational disruptions averaging <strong>3-5 days per incident</strong>. These disruptions resulted in maintenance costs, schedule adjustments, and customer compensation averaging <strong>$450,000 per incident</strong>. Quality control variations among suppliers were identified as the primary contributing factor.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display questions with semi-transparent background
def display_question(question):
    st.markdown(
        f"""
        <div style="padding: 5px; background-color: rgba(255, 255, 255);">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display numeric input with semi-transparent background
def display_numeric_input(question, min_value, max_value, key):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    value = st.number_input("", min_value=min_value, max_value=max_value, value=min_value, key=key)
    return value

# Function to display multiple-choice questions
def display_multiple_choice(question, options, key):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    selected_option = st.radio(
        "",
        options,
        key=key,
        format_func=lambda x: f"<div style='padding: 5px; background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; margin-bottom: 5px;'>{x}</div>",
    )
    return selected_option

# Function to display importance ratings
def display_importance_ratings(question, factors, key):
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    ratings = {}
    for factor in factors:
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 5px;">
                <p style="color: black; font-weight: 900;">{factor}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        ratings[factor] = st.number_input("", min_value=1, max_value=5, value=3, key=f"{key}_{factor}")
    return ratings

# Main function for Bias Group
def bias_group():
    set_background("rwth-aachen.jpg")  # Background image
    display_header()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display scenario on the first page only
    if st.session_state.page == "Page 1":
        display_scenario()

    # Display supplier details from the second page onwards
    if st.session_state.page != "Page 1":
        display_supplier_details()

    # Display questions based on the current page
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
            <h3>{st.session_state.page}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    for question in questions[st.session_state.page]:
        display_question(question)
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a numeric input for rating questions
            min_value = 1
            max_value = 10 if "confidence" in question else 5
            st.session_state.answers[question] = display_numeric_input(question, min_value, max_value, key=question)
        elif "If Supplier B improved" in question:
            # Multiple-choice question
            options = [
                "Yes, I would switch to Supplier B",
                "No, I would stay with my original choice",
                "I originally chose Supplier B and would still choose them"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
        elif "minimum reliability percentage" in question:
            # Multiple-choice question
            options = [
                "99% or higher",
                "97-98%",
                "95-96%",
                "90-94%",
                "Below 90%"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
        elif "If a delivery delay grounds aircraft" in question:
            # Multiple-choice question
            options = [
                "Pay a 35% premium for emergency shipments, impacting quarterly profit targets",
                "Cancel revenue-generating flights until delivery, potentially losing loyal customers",
                "Maintain a larger safety stock (increasing inventory costs by 20% and reducing capital available for other investments)"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
        elif "Rate the importance of each factor" in question:
            # Importance ratings
            factors = [
                "Initial purchase price",
                "Reliability rating",
                "Lead time",
                "Lead time variability",
                "Minimum order quantity",
                "Certification standards",
                "Warranty period"
            ]
            st.session_state.answers[question] = display_importance_ratings(question, factors, key=question)
        elif "Which attribute would you be most willing to compromise on" in question:
            # Multiple-choice question
            options = [
                "Price",
                "Lead time",
                "Lead time variability",
                "Minimum order quantity",
                "Warranty period"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
        elif "Would you be willing to commit to a 2-year contract" in question:
            # Multiple-choice question
            options = ["Yes", "No", "Unsure"]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
        elif "How much would you be willing to invest" in question:
            # Multiple-choice question
            options = [
                "$0 (not willing to invest)",
                "Up to $50,000",
                "$50,001 - $100,000",
                "$100,001 - $200,000",
                "Over $200,000"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question)
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
    if st.session_state.page == "Page 6" and st.button("Submit"):
        save_to_firebase(st.session_state.answers)
        st.session_state.answers = {}
        st.session_state.page = "Page 1"  # Reset to first page after submission
        st.rerun()
    
    display_footer()

if __name__ == "__main__":
    bias_group()
