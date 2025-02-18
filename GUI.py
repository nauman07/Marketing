import streamlit as st
import pandas as pd
import os

data_file = "data.csv"

# Define questions
questions = [
    "Name",
    "Email",
    "Company",
    "Position",
    "Department",
    "What is your favorite color?",
    "How many hours do you work daily?",
    "Do you prefer tea or coffee?",
    "What is your favorite hobby?"
]

def save_to_csv(answers):
    if os.path.exists(data_file):
        df = pd.read_csv(data_file, index_col=["Name", "Email"])
    else:
        df = pd.DataFrame(columns=["Name", "Email"] + questions[2:])
    
    new_entry = pd.DataFrame([answers]).set_index(["Name", "Email"])
    df = pd.concat([df, new_entry])
    df.to_csv(data_file)

def main():
    st.title("User Questionnaire")
    
    st.write("Please answer the following questions:")
    
    user_answers = {}
    user_answers["Name"] = st.text_input("Name", "")
    user_answers["Email"] = st.text_input("Email", "")
    
    for question in questions[2:]:
        user_answers[question] = st.text_input(question, "")
    
    if st.button("Submit"):
        save_to_csv(user_answers)
        st.success("Thank you! Your responses have been recorded.")

if __name__ == "__main__":
    main()
