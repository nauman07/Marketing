import streamlit as st
import base64
import pandas as pd

# FIREBASE CONNECTION COMMENTED OUT
# from firebase_config import initialize_firebase
# db = initialize_firebase()

# Questions for Survey - Reduced to 3 pages
questions = {
    "Page 1": [
        "First Name (*)",
        "Last Name",
        "Email",
        "Designation"  # Replaced Company+Position+Department with Designation dropdown
    ],
    "Page 2": [
        "Q1. Based on the information provided, which supplier would you select for AeroConnect Airlines?",
        "Q2. Rate your confidence in this decision, considering the potential impact on aircraft availability (1 = Not at all confident, 10 = Extremely confident)",
        "Q3. If you had to distribute AeroConnect's annual orders to manage supply risk, what percentage would you allocate to each supplier? (Total must equal 100%)"
    ],
    "Page 3": [
        "Q4. Selecting a supplier with lower reliability exposes AeroConnect to significant operational disruptions, potential regulatory scrutiny, and passenger compensation claims.",
        "Q5. The hidden costs from selecting the lowest-price supplier (emergency shipments, flight cancellations, maintenance complications) often exceed the initial savings.",
        "Q6. Paying more upfront for quality avionics units protects against costly flight cancellations, emergency maintenance, and damage to AeroConnect's safety reputation.",
        "Q7. Longer and variable lead times increase the risk of grounded aircraft and lost revenue when unexpected maintenance needs arise."
    ],
    "Page 4": [
        "Q8. If Supplier B improved their reliability rating to 97% but increased their price by 10%, would you change your original supplier selection? (Note- Each 1% decrease in reliability has historically corresponded to a 15% increase in maintenance issues)",
        "Q9. What is the minimum reliability percentage you would consider acceptable? (Each reliability percentage point below 99% correlates with approximately 3 additional flight cancellations per year)",
        "Q10. If a delivery delay grounds aircraft and disrupts operations, which option would you prefer?",
        "Q11. Rate the importance of each factor in your supplier selection decision: (1 = Not Important, 5 = Extremely Important)",
        "Q12. Which attribute would you be most willing to compromise on to improve reliability by 2%?"
    ],
    "Page 5": [
        "Q13. Would you be willing to commit to a 2-year contract with your chosen supplier in exchange for a 12% price reduction? (Note- This would protect against any potential future price increases due to market volatility)",
        "Q14. How much would you be willing to invest in additional quality testing equipment that could detect potential defects before installation?"
    ]
}

# Supplier details
suppliers = {
    "Price": {
        "Supplier A": "$8,750/unit (25% above market average)",
        "Supplier B": "$7,000/unit (Industry Benchmark)",
        "Supplier C": "$9,800/unit (40% above market average)"
    },
    "Lead Time": {
        "Supplier A": "18 days (±4 days variability)",
        "Supplier B": "20 days (±7 days variability)",
        "Supplier C": "15 days (±2 days variability)"
    },
    "Reliability": {
        "Supplier A": "97% defect-free rate",
        "Supplier B": "95% defect-free rate",
        "Supplier C": "99% defect-free rate"
    },
    "Minimum Order Quantity": {
        "Supplier A": "15 units",
        "Supplier B": "10 units",
        "Supplier C": "20 units"
    },
    "Additional": {
        "Supplier A": "FAA-certified manufacturing facility, 5-year warranty",
        "Supplier B": "Recently ISO 9001 certified, 2-year warranty",
        "Supplier C": "Used by 7 of the top 10 global airlines, 7-year warranty"
    }
}

# Convert supplier data to a pandas DataFrame
suppliers_df = pd.DataFrame(suppliers)
suppliers_df.index.name = "Feature"
suppliers_df.reset_index(inplace=True)

# FIREBASE FUNCTION COMMENTED OUT
# def save_to_firebase(answers):
#     try:
#         user_name = answers.get("First Name (Mandatory)", "Unknown")
#         collection_name = f"survey_{user_name.replace(' ', '_')}"
#         processed_answers = {q: (answers.get(q, "N/A") or "N/A") for q in answers}
#         processed_answers["is_control"] = False  # Mark as Bias Group
#         db.collection(collection_name).add(processed_answers)
#         st.success("Data successfully saved to Firebase!")
#     except Exception as e:
#         st.error(f"Error saving data: {e}")

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
            <h1 style="color: white;">Survey: Supplier Selection for Aircraft CDU</h1>
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
            <p style="color: black;">© 2025 RWTH Aachen University. All rights reserved.</p>
            <p style="color: black;">For more information or if you are facing any issues, please contact the developer:</p>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <img src="data:image/jpeg;base64,{image_base64}" alt="Developer Logo" width="50" style="border-radius: 50%;">
                <div>
                    <p style="margin: 0; color: black;"><strong>HarshVardhan Kanthode</strong></p>
                    <p style="margin: 0;">
                        <a href="mailto:harshvardhan.kanthode@rwth-aachen.de" style="text-decoration: none; color: black;">📧 Email</a> | 
                        <a href="https://www.linkedin.com/in/harshvardhan-kanthode-628863189/" target="_blank" style="text-decoration: none; color: black;">🔗 LinkedIn</a>
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display supplier details as a popup
def display_supplier_details_popup():
    # Initialize the session state if it doesn't exist
    if "show_supplier_details" not in st.session_state:
        st.session_state.show_supplier_details = True
    
    # Toggle button - changes label based on current state
    button_label = "Hide Supplier Details" if st.session_state.show_supplier_details else "Show Supplier Details"
    
    if st.button(button_label):
        # Toggle the state when clicked
        st.session_state.show_supplier_details = not st.session_state.show_supplier_details
        st.rerun()  # Rerun to update the UI with the new state
    
    # Show the popup if the state is True
    if st.session_state.show_supplier_details:
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
                    color: black;
                }}
                th {{
                    background-color: rgba(255, 255, 255);
                    color: black;
                }}
                </style>
                {table_html}
            </div>
            """,
            unsafe_allow_html=True
        )

# Function to display scenario
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

# Function to display multiple-choice questions horizontally with optimized styling
def display_horizontal_choice(options, key, horizontal=True):
    st.markdown(
        """
        <style>
        .stRadio > div {
            background-color: pink;
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
        horizontal=horizontal
    )
    return selected_option

# Function to display a dropdown
def display_dropdown(question, options, key):
    st.markdown(
        """
        <style>
        /* Style the selectbox container */
        div[data-testid="stSelectbox"] {
            background-color: white;
            padding: 2px;  /* Internal spacing within the container */
            border-radius: 2px;
        }
        /* Target the first child element inside the selectbox container 
           to remove any top margin/padding */
        div[data-testid="stSelectbox"] > div {
            margin-top: 0px !important;
            padding-top: -3px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    selected_option = st.selectbox(
        "",
        options,
        key=key
    )
    return selected_option

# Function to display slider with reduced distance
def display_slider(question, min_value, max_value, key):
    # Apply white background and padding for better visibility
    st.markdown(
        """
        <style>
        div[data-testid="stSlider"] {
            background-color: pink;
            padding: 5px 20px;  /* Reduced padding */
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

# # Function to display percentage allocation using sliders
# def display_percentage_allocation_sliders():
#     # Initialize session state for percentages
#     if "supplier_a_percent" not in st.session_state:
#         st.session_state.supplier_a_percent = 33
#     if "supplier_b_percent" not in st.session_state:
#         st.session_state.supplier_b_percent = 33
#     if "supplier_c_percent" not in st.session_state:
#         st.session_state.supplier_c_percent = 34

#     # Function to adjust percentages dynamically
#     def adjust_percentages(changed_supplier):
#         total = st.session_state.supplier_a_percent + st.session_state.supplier_b_percent + st.session_state.supplier_c_percent
#         if total != 100:
#             if changed_supplier == "A":
#                 remaining = 100 - st.session_state.supplier_a_percent
#                 st.session_state.supplier_b_percent = remaining // 2
#                 st.session_state.supplier_c_percent = remaining - st.session_state.supplier_b_percent
#             elif changed_supplier == "B":
#                 remaining = 100 - st.session_state.supplier_b_percent
#                 st.session_state.supplier_a_percent = remaining // 2
#                 st.session_state.supplier_c_percent = remaining - st.session_state.supplier_a_percent
#             elif changed_supplier == "C":
#                 remaining = 100 - st.session_state.supplier_c_percent
#                 st.session_state.supplier_a_percent = remaining // 2
#                 st.session_state.supplier_b_percent = remaining - st.session_state.supplier_a_percent
    
#     # Create a row of three sliders
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.session_state.supplier_a_percent = st.slider(
#             "Supplier A",
#             min_value=0,
#             max_value=100,
#             value=st.session_state.supplier_a_percent,
#             key="supplier_a_slider",
#             on_change=adjust_percentages,
#             args=("A",)
#         )

#     with col2:
#         st.session_state.supplier_b_percent = st.slider(
#             "Supplier B",
#             min_value=0,
#             max_value=100,
#             value=st.session_state.supplier_b_percent,
#             key="supplier_b_slider",
#             on_change=adjust_percentages,
#             args=("B",)
#         )

#     with col3:
#         st.session_state.supplier_c_percent = st.slider(
#             "Supplier C",
#             min_value=0,
#             max_value=100,
#             value=st.session_state.supplier_c_percent,
#             key="supplier_c_slider",
#             on_change=adjust_percentages,
#             args=("C",)
#         )

#     # Display current allocation and total
#     total_percent = st.session_state.supplier_a_percent + st.session_state.supplier_b_percent + st.session_state.supplier_c_percent
#     st.markdown(
#         f"""
#         <div style="padding: 5px; background-color: rgba(255, 255, 255);">
#             <p style="color: black; font-weight: 900; margin-bottom: 5px;">
#                 Current Allocation: Supplier A = {st.session_state.supplier_a_percent}%, Supplier B = {st.session_state.supplier_b_percent}%, Supplier C = {st.session_state.supplier_c_percent}%
#             </p>
#             <p style="color: black; font-weight: 900; margin-bottom: 5px;">
#                 Total: {total_percent}%
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # Save the answers to session state
#     st.session_state.answers["Supplier A: in %"] = st.session_state.supplier_a_percent
#     st.session_state.answers["Supplier B: in %"] = st.session_state.supplier_b_percent
#     st.session_state.answers["Supplier C: in %"] = st.session_state.supplier_c_percent

def display_percentage_allocation_sliders():
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    
    # Initialize session state for percentages (only if not already set)
    if "supplier_a_percent" not in st.session_state:
        st.session_state.supplier_a_percent = 0
    if "supplier_b_percent" not in st.session_state:
        st.session_state.supplier_b_percent = 0
    if "supplier_c_percent" not in st.session_state:
        st.session_state.supplier_c_percent = 0

    # Add CSS that targets only the individual slider containers
    st.markdown(
        """
        <style>
        /* Target individual sliders but not their parent container */
        div[data-testid="column"] div[data-testid="stSlider"] {
            background-color: pink;
            padding: 5px 20px;
            border-radius: 5px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Create a row of three sliders
    col1, col2, col3 = st.columns(3)
    
    # Use the sliders without modifying session state directly in assignment
    with col1:
        a_percent = st.slider(
            "Supplier A",
            min_value=0,
            max_value=100,
            step=5,  # This ensures increments of 5
            value=st.session_state.supplier_a_percent,
            key="supplier_a_slider"
        )

    with col2:
        b_percent = st.slider(
            "Supplier B",
            min_value=0,
            max_value=100,
            step=5,  # This ensures increments of 5
            value=st.session_state.supplier_b_percent,
            key="supplier_b_slider"
        )

    with col3:
        c_percent = st.slider(
            "Supplier C",
            min_value=0,
            max_value=100,
            step=5,  # This ensures increments of 5
            value=st.session_state.supplier_c_percent,
            key="supplier_c_slider"
        )
    
    # Update session state after all sliders are rendered
    st.session_state.supplier_a_percent = a_percent
    st.session_state.supplier_b_percent = b_percent
    st.session_state.supplier_c_percent = c_percent

    # Display current allocation and total
    total_percent = a_percent + b_percent + c_percent
    
    # Check if total exceeds 100%
    if total_percent != 100:
        color = "red"
        warning_message = " (Please adjust to equal 100%)"
    else:
        color = "black"
        warning_message = ""
    
    st.markdown(
        f"""
        <div style="padding: 5px; background-color: rgba(255, 255, 255);">
            <p style="color: {color}; font-weight: 900; margin-bottom: 5px;">
                Total: {total_percent}% (A: {a_percent}%, B: {b_percent}%, C: {c_percent}%){warning_message}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Add this to session state for validation
    st.session_state.allocation_valid = (total_percent == 100)

    # Save the answers to session state
    st.session_state.answers["Supplier A: in %"] = a_percent
    st.session_state.answers["Supplier B: in %"] = b_percent
    st.session_state.answers["Supplier C: in %"] = c_percent

# Function to display importance ratings with a 2x3 matrix of sliders for space optimization
def display_importance_ratings_matrix(question, factors, key):
    # Add CSS for styling
    st.markdown(
        """
        <style>
        /* Style for the entire slider component including label */
        div[data-testid="stSlider"] {
            background-color: pink;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create a 2x3 matrix layout
    ratings = {}
    
    # First row - 3 factors
    col1, col2, col3 = st.columns(3)
    with col1:
        # Use the label parameter to include the factor name
        ratings[factors[0]] = st.slider(
            label=factors[0],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[0]}"
        )
    
    with col2:
        ratings[factors[1]] = st.slider(
            label=factors[1],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[1]}"
        )
    
    with col3:
        ratings[factors[2]] = st.slider(
            label=factors[2],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[2]}"
        )
    
    # Second row - 4 factors
    col4, col5, col6, col7 = st.columns(4)
    with col4:
        ratings[factors[3]] = st.slider(
            label=factors[3],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[3]}"
        )
    
    with col5:
        ratings[factors[4]] = st.slider(
            label=factors[4],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[4]}"
        )
    
    with col6:
        ratings[factors[5]] = st.slider(
            label=factors[5],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[5]}"
        )
    
    with col7:
        ratings[factors[6]] = st.slider(
            label=factors[6],
            min_value=1, 
            max_value=5, 
            value=3, 
            key=f"{key}_{factors[6]}"
        )
    
    return ratings
# 2. Fix for the navigation buttons and validation
def navigation_buttons():
    FIRST_NAME_FIELD = "First Name (*)"
    
    # Inject custom CSS to remove padding from columns (Streamlit's container elements)
    st.markdown(
    """
    <style>
    /* This targets the column container (the selector may vary across Streamlit versions) */
    div[data-testid="column"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    # Add spacing before navigation buttons
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Create a 3-column layout with the last column much wider to push the button right
    col1, spacer, col3 = st.columns([1, 5, 1])
    
    pages = list(questions.keys())
    current_index = pages.index(st.session_state.page)
    is_last_page = current_index == len(pages) - 1  # Check if on last page
    
    # Previous button in first column
    if current_index > 0:
        if col1.button("Previous"):
            st.session_state.page = pages[current_index - 1]
            st.rerun()
    
    # Next button in third column - only show if not on the last page
    if not is_last_page:
        next_clicked = col3.button("Next", key="real_next")
        
        if next_clicked:
            message = ""  # Initialize message variable
            
            # Validation for Page 1 - First Name is mandatory
            if st.session_state.page == "Page 1":
                first_name = st.session_state.answers.get(FIRST_NAME_FIELD, "")
                if first_name.strip() == "":
                    message = "First Name is mandatory. Please fill it before proceeding."
                else:
                    st.session_state.page = pages[current_index + 1]
                    st.rerun()
            
            # Validation for Page 2 - Total allocation must be 100%
            elif st.session_state.page == "Page 2":
                if "allocation_valid" in st.session_state and not st.session_state.allocation_valid:
                    message = "Please ensure the total allocation equals 100% before proceeding."
                else:
                    st.session_state.page = pages[current_index + 1]
                    st.rerun()
            
            # No validation required for other pages
            else:
                st.session_state.page = pages[current_index + 1]
                st.rerun()
            
            # Display error message inside a styled box if validation fails
            if message:
                st.markdown(
                    f"""
                    <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.9); 
                                border-radius: 10px; margin-bottom: 10px; border: 1px solid red;">
                        <p style="color: red; font-weight: bold;">⚠️ {message}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Submit button (only on the last page) - placed in the same column as the Next button would be
    if is_last_page:
        submit_clicked = col3.button("Submit")
        if submit_clicked:
            st.markdown(
                """
                <div style="padding: 10px; background-color: rgba(255, 255, 255, 0.9); 
                            border-radius: 10px; margin-bottom: 10px; border: 1px solid green;">
                    <p style="color: green; font-weight: bold;">✅ Survey submitted successfully! Thank you for your participation.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.session_state.answers = {}
            st.session_state.page = "Page 1"  # Reset to first page after submission
            st.rerun()
            
# Main function for the survey
def main():
    set_background("rwth-aachen.jpg")  # Background image
    display_header()

    # Inject custom CSS to reduce spacing
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] { margin-top: -20px; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Inject custom CSS to reduce spacing
    st.markdown(
        """
        <style>
        div[data-testid="stRadio"] { margin-top: -35px; }
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

    # Display supplier details as a popup button on every page
    display_supplier_details_popup()

    # # Display questions based on the current page
    # st.markdown(
    #     f"""
    #     <div style="padding: 10px; background-color: rgba(255, 255, 255); border-radius: 10px; margin-bottom: 10px;">
    #         <h3 style="color: black;">{st.session_state.page}</h3>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
    
    # For Page 3, display the common remark for scale at the top
    if st.session_state.page == "Page 3":
        st.markdown(
            """
            <div style="padding: 5px; background-color: rgba(255, 255, 255); border-radius: 5px; margin-bottom: 10px;">
                <p style="color: black; font-style: italic;">
                    <strong>Note:</strong> Rate the following questions (Q4-Q7) from a scale of 1-5 (1 = Strongly Disagree/Not Important, 5 = Strongly Agree/Extremely Important)
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Process questions for the current page
    for question in questions[st.session_state.page]:
        display_question(question)
        
        # For Designation, use dropdown instead of text fields
        if question == "Designation":
            options = [
                "1. Director/Manager",
                "2. Professor/Researcher",
                "3. Student",
                "4. Consultant/Entry Level"
            ]
            st.session_state.answers[question] = display_dropdown(question, options, key=question)
        
        # For Q1 (supplier selection), display options horizontally
        elif "Q1. Based on the information provided" in question:
            options = ["Supplier A", "Supplier B", "Supplier C"]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=True)
        
        # For Q3 (percentage allocation), use sliders
        elif "Q3. If you had to distribute AeroConnect's" in question:
            display_percentage_allocation_sliders()
        
        # For rating questions with confidence or agree/disagree scale
        elif any(q in question for q in ["Q2","Q4", "Q5", "Q6", "Q7", "Q11"]):
            min_value = 1
            max_value = 10 if "confidence" in question else 5
            st.session_state.answers[question] = display_slider(question, min_value, max_value, key=question)
        
        # For Q8 (supplier improvement), display options horizontally
        elif "If Supplier B improved" in question:
            options = [
                "Yes, I would switch to Supplier B",
                "No, I would stay with my original choice",
                "I originally chose Supplier B and would still choose them"
            ]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=False)
        
        # For Q9 (reliability percentage), display options horizontally
        elif "minimum reliability percentage" in question:
            options = [
                "99% or higher",
                "97-98%",
                "95-96%",
                "90-94%",
                "Below 90%"
            ]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=True)
        
        # For Q10 (delivery delay), display options horizontally
        elif "If a delivery delay grounds aircraft" in question:
            options = [
                "Pay a 35% premium for emergency shipments",
                "Cancel revenue-generating flights until delivery",
                "Maintain a larger safety stock (20% increase in inventory costs)"
            ]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=False)
        
        # For Q11 (importance ratings), use a matrix of sliders
        elif "Rate the importance of each factor" in question:
            factors = [
                "Initial price",
                "Reliability",
                "Lead time",
                "Lead variability",
                "Minimum order",
                "Certification",
                "Warranty"
            ]
            st.session_state.answers[question] = display_importance_ratings_matrix(question, factors, key=question)
        
        # For Q12 (compromise attribute), display options horizontally
        elif "Which attribute would you be most willing to compromise on" in question:
            options = [
                "Price",
                "Lead time",
                "Lead time variability",
                "Minimum order quantity",
                "Warranty period"
            ]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=False)
        
        # For Q13 (contract commitment), display options horizontally
        elif "Would you be willing to commit to a 2-year contract" in question:
            options = ["Yes", "No", "Unsure"]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=True)
        
        # For Q14 (investment), display options horizontally
        elif "How much would you be willing to invest" in question:
            options = [
                "$0 (not willing to invest)",
                "Up to $50,000",
                "\$50,001 - \$100,000",
                "\$100,001 - \$200,000",
                "Over $200,000"
            ]
            st.session_state.answers[question] = display_horizontal_choice(options, key=question, horizontal=False)
        
        # For all other questions (like name, email), use text input
        else:
            st.session_state.answers[question] = st.text_input("", value=st.session_state.answers.get(question, ""), key=question)
    
    # # Navigation buttons
    # col1, col2, col3 = st.columns(3)
    
    # pages = list(questions.keys())
    # current_index = pages.index(st.session_state.page)
    
    # if current_index > 0 and col1.button("Previous"):
    #     st.session_state.page = pages[current_index - 1]
    #     st.rerun()
    
    # # Next button on Page 1 no longer checks for filled information
    # if current_index < len(pages) - 1 and col3.button("Next"):
    #     st.session_state.page = pages[current_index + 1]
    #     st.rerun()
    
    # # Submit button
    # if st.session_state.page == "Page 5" and st.button("Submit"):
    #     # Firebase connection commented out, so just show success message
    #     st.success("Survey submitted successfully! Thank you for your participation.")
    #     st.session_state.answers = {}
    #     st.session_state.page = "Page 1"  # Reset to first page after submission
    #     st.rerun()
    navigation_buttons()
    
    display_footer()

if __name__ == "__main__":
    main()
