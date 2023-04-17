import streamlit as st

st.title("Upload Datasets")
st.title("")

uploadFile_users = st.file_uploader('Step1: Upload Books Dataset (*.csv)')
uploadFile_ratings = st.file_uploader('Step1: Upload Ratings Dataset (*.csv)')

st.title("")
st.button('Process')