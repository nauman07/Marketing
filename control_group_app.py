import streamlit as st
from firebase_config import initialize_firebase

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

# Function to display questions with grey background
def display_question(question):
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <p style="color: black; font-weight: 900;">{question}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main function for Control Group
def control_group():
    st.title("Control Group Survey")

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Page 1"
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Display questions based on the current page
    st.write(f"### {st.session_state.page}")
    for question in questions[st.session_state.page]:
        display_question(question)
        if "Rate your confidence" in question or "Strongly Disagree" in question:
            # Use a slider for rating questions
            st.session_state.answers[question] = st.slider("", 1, 10 if "confidence" in question else 5, key=question)
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

if __name__ == "__main__":
    control_group()
