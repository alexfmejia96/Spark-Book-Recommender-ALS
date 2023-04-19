import streamlit as st

def main():
    st.set_page_config(
        page_title="Group 7",
        page_icon="books",
        initial_sidebar_state="expanded"
    )

if __name__ == "__main__":
    main()


from components.custom import *

#update_pages_names()
add_constant_elements("Welcome to our web app, designed to provide personalized book recommendations.")