import streamlit as st
from firebase_config import initialize_firebase
import base64
import pandas as pd

# Initialize Firebase
db = initialize_firebase()

# Questions for Control Group
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
        "Q1. Based on the information provided, which supplier would you select for AeroConnect Airlines?",
        "Q2. Rate your confidence in this decision, considering the potential impact on aircraft availability (1 = Not at all confident, 10 = Extremely confident)",
        "Q3. If you had to distribute AeroConnect's annual orders to manage supply risk, what percentage would you allocate to each supplier? (Total must equal 100%)",
        "Supplier A: in %",
        "Supplier B: in %",
        "Supplier C: in %"
    ],
    "Page 3": [
        "Q4. Selecting a supplier with lower reliability exposes AeroConnect to significant operational disruptions, potential regulatory scrutiny, and passenger compensation claims. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "Q5. The hidden costs from selecting the lowest-price supplier (emergency shipments, flight cancellations, maintenance complications) often exceed the initial savings. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "Q6. Paying more upfront for quality avionics units protects against costly flight cancellations, emergency maintenance, and damage to AeroConnect's safety reputation. (1 = Strongly Disagree, 5 = Strongly Agree)",
        "Q7. Longer and variable lead times increase the risk of grounded aircraft and lost revenue when unexpected maintenance needs arise. (1 = Strongly Disagree, 5 = Strongly Agree)"
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

# Function to display questions with reduced distance and no background on options
def display_question(question):
    st.markdown(
        f"""
        <div style="padding: 5px; background-color: rgba(255, 255, 255);">
            <p style="color: black; font-weight: 900; margin-bottom: 5px;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display numeric input with reduced distance
def display_slider(question, min_value, max_value, key):
    # Apply white background and padding for better visibility
    st.markdown(
        """
        <style>
        div[data-testid="stSlider"] {
            background-color: white;
            padding: 5px;  /* Reduced padding */
            border-radius: 5px;
        }
        
        /* Adjusts the label and internal padding */
        div[data-testid="stSlider"] > div {
            margin: 0px !important;
            padding: 0px !important;
        }

        /* Reduce space between slider elements */
        div[data-testid="stSlider"] .stSlider {
            gap: 2px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Create the slider
    value = st.slider("", min_value=min_value, max_value=max_value, value=(min_value + max_value) // 2, key=key)
    return value

# Function to display multiple-choice questions with white background for options
def display_multiple_choice(question, options, key):
    st.markdown(
        """
        <style>
        .stRadio > div {
            background-color: white;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    selected_option = st.radio(
        "",
        options,
        key=key,
    )
    return selected_option

def display_percentage_allocation():
    # Initialize session state for percentages
    if "supplier_a_percent" not in st.session_state:
        st.session_state.supplier_a_percent = 33
    if "supplier_b_percent" not in st.session_state:
        st.session_state.supplier_b_percent = 33
    if "supplier_c_percent" not in st.session_state:
        st.session_state.supplier_c_percent = 34

    # Function to adjust percentages dynamically
    def adjust_percentages(changed_supplier):
        total = st.session_state.supplier_a_percent + st.session_state.supplier_b_percent + st.session_state.supplier_c_percent
        if total != 100:
            if changed_supplier == "A":
                remaining = 100 - st.session_state.supplier_a_percent
                st.session_state.supplier_b_percent = remaining // 2
                st.session_state.supplier_c_percent = remaining - st.session_state.supplier_b_percent
            elif changed_supplier == "B":
                remaining = 100 - st.session_state.supplier_b_percent
                st.session_state.supplier_a_percent = remaining // 2
                st.session_state.supplier_c_percent = remaining - st.session_state.supplier_a_percent
            elif changed_supplier == "C":
                remaining = 100 - st.session_state.supplier_c_percent
                st.session_state.supplier_a_percent = remaining // 2
                st.session_state.supplier_b_percent = remaining - st.session_state.supplier_a_percent
    
    # Add a space between the previous text box and the slider columns
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Sliders for percentage allocation
    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.supplier_a_percent = st.slider(
            "Supplier A: in %",
            min_value=0,
            max_value=100,
            value=st.session_state.supplier_a_percent,
            key="supplier_a_slider",
            on_change=adjust_percentages,
            args=("A",)
        )

    with col2:
        st.session_state.supplier_b_percent = st.slider(
            "Supplier B: in %",
            min_value=0,
            max_value=100,
            value=st.session_state.supplier_b_percent,
            key="supplier_b_slider",
            on_change=adjust_percentages,
            args=("B",)
        )

    with col3:
        st.session_state.supplier_c_percent = st.slider(
            "Supplier C: in %",
            min_value=0,
            max_value=100,
            value=st.session_state.supplier_c_percent,
            key="supplier_c_slider",
            on_change=adjust_percentages,
            args=("C",)
        )

    # Display current allocation and total
    total_percent = st.session_state.supplier_a_percent + st.session_state.supplier_b_percent + st.session_state.supplier_c_percent
    st.markdown(
        f"""
        <div style="padding: 5px; background-color: rgba(255, 255, 255);">
            <p style="color: black; font-weight: 900; margin-bottom: 5px;">
                Current Allocation: Supplier A = {st.session_state.supplier_a_percent}%, Supplier B = {st.session_state.supplier_b_percent}%, Supplier C = {st.session_state.supplier_c_percent}%
            </p>
            <p style="color: black; font-weight: 900; margin-bottom: 5px;">
                Total: {total_percent}%
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Save the answers to session state
    st.session_state.answers["Supplier A: in %"] = st.session_state.supplier_a_percent
    st.session_state.answers["Supplier B: in %"] = st.session_state.supplier_b_percent
    st.session_state.answers["Supplier C: in %"] = st.session_state.supplier_c_percent

# Main function for Control Group
def control_group():
    set_background("rwth-aachen.jpg")  # Background image
    display_header()

    # Inject custom CSS to reduce spacing before any questions are displayed
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] { margin-top: -20px; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
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

        if "Q3. If you had to distribute AeroConnect's" in question:
            display_percentage_allocation()  # Call the custom function for percentage allocation
        
        elif "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a numeric input for rating questions
            min_value = 1
            max_value = 10 if "confidence" in question else 5
            st.session_state.answers[question] = display_slider(question, min_value, max_value, key=question)
        elif "which supplier would you select for AeroConnect" in question:
            options = [
                "Supplier A",
                "Supplier B",
                "Supplier C"
            ]
            st.session_state.answers[question] = display_multiple_choice(question, options, key=question) 
        else:
            # Use a text input for other questions
            st.session_state.answers[question] = st.text_input(" ", value=st.session_state.answers.get(question, ""), key=question)

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
