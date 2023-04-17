import streamlit as st
import pandas as pd
from components.custom import *

#st.set_page_config(layout='wide')
recommendations_get_style()

@st.cache_data
def load_data(url, **kwargs):
    df = pd.read_parquet(url, **kwargs)
    return df


books = load_data('data/books.parquet')
book_pairs = load_data('data/recommendations/non_personalized.parquet')

with st.sidebar:
    with st.container():
        st.header('Book Recommedations')
        recommend_mode = st.radio('',
        [   'From Book Names',
            'From User Preferences'
        ], key='radio')

st.header("Books to use as Recommendations Basis")
st.header('')

cols_placeholder = st.empty()
st.header("")
st.header("Recommendations")

if recommend_mode == 'From Book Names':
    c1, c2 = st.columns([8, 2])
    with c1:
        sel_books = st.multiselect('Selected Books', books.title.unique())
    with c2:
        recommends_count = st.selectbox('Books to recommmed', range(1, 11), index=3)

    if len(sel_books) > 0:
        with cols_placeholder:
            book_grid(sel_books, books, 'title')
        
        recommends = books_np_recommends(books.set_index('title').loc[sel_books].isbn13, book_pairs, recommends_count)
        book_grid(recommends, books, 'isbn13')
        





