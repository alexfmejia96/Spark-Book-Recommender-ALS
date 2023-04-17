import streamlit as st
import pandas as pd

def recommendations_get_style():
    style = st.markdown("""
        <style>
        .stRadio > label {
            min-height: 0px;
        }

        .book-container {
            text-align: block;
            height: 240x;
            width: 100%;
            position: relative;
            text-align: center;
            padding: 10px 0px 0px 0px;
            white-space: nowrap; 
        }

        .book-container img {
            height: 120px;
        }

        .book-container span {
            font-family: "Source Sans Pro", sans-serif;
            color: rgba(250, 250, 250, 0.6);
            font-size: 10px;
            display: block;
            margin: 10px;
        }

        .grid-container {
            grid-gap: 20px;
            display: grid;
            grid-template-columns: repeat(6, 100px);
            grid-template-rows: repeat(1, 170px);
            margin: 10px 0px 20px 0px;
            height: fit-content;
        }

        .grid-item {
            background-color: rgba(0, 0, 0, 0.4);
            height: fit-content;
        }

        .truncate {
            overflow: hidden;
            text-overflow: ellipsis;
        }
        </style>""", unsafe_allow_html=True)
    return style

def book_container(book_match, books, col_name):
    book = books[books[col_name] == book_match].iloc[0]
    container = st.container()
    element_html = f''' <div class="grid-item">
                            <div class="book-container">
                                <img src="{book.image}">
                                <span class="truncate" title="{book.title}">{book.title}</span>
                            </div>
                        </div>'''
    return element_html

def book_grid(book_list, books, col_name):
    element_html = '<div class="grid-container">'

    for book_match in book_list:
        element_html = element_html + book_container(book_match, books, col_name)
    
    element_html = element_html + '</div>'
    return st.markdown(element_html, unsafe_allow_html=True)

def book_np_recommends(isbn13, book_pairs, count):
    
    recommends = book_pairs.query(f'book_a == {isbn13} | book_b == {isbn13}')
    count = min(count, len(recommends))
    recommends = [(book.book_a if book.book_a != isbn13 else book.book_b, book['0']) for book in recommends[:count].iloc]

    if count == 0:
        return None
    else:
        return pd.DataFrame(recommends, columns=['book', 'count'])

def books_np_recommends(isbn13_list, book_pairs, count):
    recommends = pd.concat([book_np_recommends(isbn13, book_pairs, count) for isbn13 in isbn13_list])\
        .drop_duplicates(keep='first')\
        .sort_values(['count'], ascending=False)

    count = min(count, len(recommends))
    
    if count == 0:
        return None
    else:
        return pd.DataFrame(recommends, columns=['book', 'count'])[:count].book.values
