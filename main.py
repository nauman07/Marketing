import streamlit as st
import random

# Import the main functions from the two apps
from control_group_app import main as control_group_main
from bias_test import main as bias_test_main

def main():
    st.set_page_config(page_title="Main App", page_icon="📊")

    # Store selected app in session state
    if "selected_app" not in st.session_state:
        st.session_state.selected_app = random.choice(["control", "bias"])

    # Run the selected app
    if st.session_state.selected_app == "control":
        control_group_main()
    else:
        bias_test_main()

if __name__ == "__main__":
    main()
