import streamlit as st
from components.custom import *

st.set_page_config(
    page_title="Group 7: Book Recommender",
    page_icon="books",
)

update_pages_names()
add_constant_elements("Welcome to our web app, designed to provide personalized book recommendations.")