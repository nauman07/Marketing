import streamlit as st
import random

# Import the main functions from the two apps
from control_group_app import main as control_group_main
from bias_test import main as bias_test_main

def main():
    st.set_page_config(page_title="Main App", page_icon="📊")

    # Randomly select one of the two apps
    selected_app = random.choice([control_group_main, bias_test_main])
  
    # Run the selected app
    selected_app()

if __name__ == "__main__":
    main()
