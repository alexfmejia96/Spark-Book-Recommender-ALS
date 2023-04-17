import streamlit as st
import pandas as pd
#from sklearn.linear_model import LinearRegression
import numpy
#import matplotlib.pyplot stas plt
from pandas.plotting import scatter_matrix
from itertools import permutations

st.title("Data Analysis")
st.text("Please enter the book name and upload analyzing files and then press button to start.")
startAnalysis = st.sidebar.button("Start analysis")

st.header('Enter a book name')
bookname = st.text_input(label = "Please enter a book name you like and we can start book recommandation from there" )

st.header('Upload Files for Analysis')
uploadFile_users = st.file_uploader('Step1: Upload Users File')
uploadFile_ratings = st.file_uploader('Step2: Upload Ratings File')
#uploadFile_books = st.file_uploader('Step3: Upload Books File')
#uploadFile_books_ratings = st.file_uploader('Step4: Upload Books and Ratings Merge File')
uploaded_files_books = st.file_uploader('Step3: Upload multiple book files',accept_multiple_files=True)


if uploadFile_users is not None:
    users = pd.read_csv(uploadFile_users)

if uploadFile_ratings is not None:
    ratings = pd.read_csv(uploadFile_ratings)
    ratings.columns = ratings.columns.str.replace('-','_').str.lower()

if uploaded_files_books is not None:  
    for f in uploaded_files_books:
        st.write(f)
    data_list = []
    for f in uploaded_files_books:
        data = pd.read_csv(f)
        data_list.append(data)
    




#if uploadFile_books is not None:
#    books = pd.read_csv(uploadFile_books)
#    books.astype(str)
    #books = books.dropna(subset=["publisher", "authors", "language", "title"])

#if uploadFile_books_ratings is not None:
#    ratings_books = pd.read_csv(uploadFile_books_ratings)


if startAnalysis:
    st.header('Summary of Input Tables')
    books = pd.concat(data_list)
    books = books.dropna(subset=["publisher", "authors", "language", "title"])
    
    st.write(users.describe())
    st.write(ratings.describe())
    #st.write(books.describe())
    st.write(books.head())

    st.header('Most Popular Items')
    st.write(books["title"].value_counts())
    explicit_rating = ratings.query("book_rating != 0")
    st.write(explicit_rating.head())

    st.header('Merge Ratings and Books')
    ratings_books = explicit_rating.merge(books, on=["isbn"])
    #st.write(ratings_books.info())
    ratings_books = ratings_books[["user_id", "isbn13", "title", "authors", "publisher", "language", "book_rating"]]
    st.write(ratings_books.head())

    st.subheader('Most Like Items')
    avg_rating = ratings_books[["title", "book_rating"]].groupby(["title"]).mean().sort_values(by="book_rating", ascending=False)
    st.write(avg_rating.reset_index())


    st.subheader('Average Rating of Remaining Books')
    avg_popular = ratings_books[["title", "book_rating"]].groupby("title").mean().reset_index().sort_values(by="book_rating", ascending=False)
    st.write(avg_popular)

    grouped = ratings_books.groupby("title")[["book_rating"]].agg({'book_rating' : [('num_ratings', 'count')]})
    grouped.columns = grouped.columns.droplevel()
    grouped = grouped.reset_index().sort_values(by="num_ratings", ascending=False)
    st.write(grouped) 

    st.subheader('Filter out books with fewer than 10 reviews:')
    frequency = ratings_books["title"].value_counts()
    frequently_reviewed = frequency[frequency > 10].index
    books_df = ratings_books[ratings_books["title"].isin(frequently_reviewed)]
    st.write(books_df.head())
    st.write(books_df["title"].value_counts())

    st.subheader('Filter out less common languages')
    st.text("The same process can be repeated for lanuages. There are only two books written in Russian and one in Hindi. These can be removed since no model can make reasonable predictions based on so few values. The eight books written in en_US will be merged into the en language category")
    books_df.loc[books_df["language"] == "en_US", "language"] = "en"
    minor_langs = books_df.loc[(books_df["language"] == "ru") | (books_df["language"] == "hi")].index
    books_df = books_df.drop(minor_langs, axis=0)
    st.write(books_df["language"].value_counts())

    st.subheader('Average Rating of Remaining Books')
    avg_popular = books_df[["title", "book_rating"]].groupby("title").mean().reset_index().sort_values(by="book_rating", ascending=False)
    st.write(avg_popular)

    grouped = books_df.groupby("title")[["book_rating"]].agg({'book_rating' : [('num_ratings', 'count')]})
    grouped.columns = grouped.columns.droplevel()
    grouped = grouped.reset_index().sort_values(by="num_ratings", ascending=False)
    st.write(grouped)

    st.subheader('Non-Personalized Recommendations')
    st.text('These are recommendations made to all users without taking their preferences into account. One example is to recommend items most commonly seen together. To accomplish this, record every time two books were read by the same person, and then count how often these pairings of books occur. Use the resulting lookup table to suggest books that are often read by the same people, implying that if they like one, they are likely to enjoy the other.')
    def create_pairs(col):
        """Return pairs of books that are frequently read together"""
        pairs = pd.DataFrame(list(permutations(col.values, 2)), columns=["book_a", "book_b"])
        return pairs
    book_pairs = books_df.groupby("user_id")["title"].apply(create_pairs)
    book_pairs = book_pairs.reset_index(drop=True)
    st.write(book_pairs.head())
    pair_counts = book_pairs.groupby(["book_a", "book_b"]).size()
    pair_counts_df = pair_counts.to_frame(name="size").reset_index().sort_values(by="size", ascending=False)
    true_pairs = pair_counts_df[pair_counts_df["book_a"] != pair_counts_df["book_b"]]
    st.write(true_pairs.head())

    st.subheader('Personalized Recommendations')
    st.text('Top 10 books frequently read with the book you entered')
    book_reco = true_pairs[true_pairs["book_a"] == bookname].nlargest(10, "size")
    st.write(book_reco)
#######
    #Serialize userId and bookId columns
    #books_df.user_id = pd.Categorical(books_df.user_id)
    #books_df["userId"] = books_df.user_id.cat.codes
    #books_df.isbn13 = pd.Categorical(books_df.isbn13)
    #books_df["bookId"] = books_df.isbn13.cat.codes
    #books_df = books_df.rename(columns={"book_rating": "rating"})
    #clean_df = books_df[["userId", "bookId", "title", "language", "rating"]]
    #Save to Parquet
    #clean_df.to_parquet('working_frame.parquet', index=False)
    #client.close()