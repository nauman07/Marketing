import streamlit as st
import pandas as pd
import os
from github import Github

# GitHub credentials and repository information
GITHUB_TOKEN = "your_github_personal_access_token"
REPO_NAME = "your_username/your_repo_name"
BRANCH = "main"  # or "master" depending on your repo
CSV_FILE_PATH = "data.csv"

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
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH, index_col=["Name", "Email"])
    else:
        df = pd.DataFrame(columns=["Name", "Email"] + questions[2:])
    
    new_entry = pd.DataFrame([answers]).set_index(["Name", "Email"])
    df = pd.concat([df, new_entry])
    df.to_csv(CSV_FILE_PATH)

def push_to_github():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    with open(CSV_FILE_PATH, "r") as file:
        content = file.read()
    
    try:
        contents = repo.get_contents(CSV_FILE_PATH, ref=BRANCH)
        repo.update_file(contents.path, "Update data.csv", content, contents.sha, branch=BRANCH)
    except:
        repo.create_file(CSV_FILE_PATH, "Create data.csv", content, branch=BRANCH)

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
        push_to_github()
        st.success("Thank you! Your responses have been recorded and pushed to GitHub.")

if __name__ == "__main__":
    main()
