import streamlit as st
import pandas as pd
from components.custom import *

update_pages_names()
recommendations_get_style()

@st.cache_data
def load_data(url, **kwargs):
    df = pd.read_parquet(url, **kwargs)
    return df

books = load_data('data/books.parquet')
book_pairs = load_data('data/recommendations/non_personalized.parquet')

add_constant_elements('Welcome, stranger!')

with st.sidebar:
    st.sidebar.title("Choose your role")
    with st.container():
        recommend_mode = st.radio('',
        [   'Unregistered User',
            'Registered User',
            'Librarian'
        ], key='radio')

if recommend_mode == 'Unregistered User':

    st.header("Books to use as Recommendations Basis")
    st.header('')

    cols_placeholder = st.empty()
    with cols_placeholder:
        st.caption('Please enter a book name you like and we can start book recommendation from there.')

    c1, c2 = st.columns([8, 2])
    with c1:
        sel_books = st.multiselect('Select Books', books.title.unique())
    with c2:
        recommends_count = st.selectbox('Books to recommend', range(1, 11), index=3)

    if len(sel_books) > 0:
        st.header("")
        st.header("Recommendations")

        with cols_placeholder:
            book_grid(sel_books, books, 'title')
        
        recommends = books_np_recommends(books.set_index('title').loc[sel_books].isbn13, book_pairs, recommends_count)
        book_grid(recommends, books, 'isbn13')
