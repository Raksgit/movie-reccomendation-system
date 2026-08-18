import time
import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# PAGE CONFIG
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# NETFLIX STYLE CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #0b0b0f, #141414);
    color: white;
}

.main {
    background-color: #0b0b0f;
}

/* Main title */
h1 {
    color: #e50914;
    text-align: center;
    font-size: 45px;
    font-weight: 800;
}

/* Section headings */
h2, h3 {
    color: white;
}

/* Search box */
div[data-baseweb="input"] {
    background-color: #222222;
    border: 1px solid #555555;
    border-radius: 8px;
}

input {
    color: white !important;
}

/* Recommend button */
.stButton > button {
    width: 100%;
    background-color: #e50914;
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: bold;
    padding: 10px;
}

.stButton > button:hover {
    background-color: #b20710;
}

/* Movie title */
.movie-title {
    text-align: center;
    font-size: 15px;
    font-weight: bold;
    color: white;
    margin-top: 8px;
}

/* Rating */
.rating {
    text-align: center;
    color: #ffd700;
    font-weight: bold;
    font-size: 13px;
}

/* Similarity */
.similarity {
    text-align: center;
    color: #aaaaaa;
    font-size: 12px;
}

hr {
    border-color: #333333;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    "<h1>🎬 Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#aaaaaa;font-size:18px;'>"
    "Discover movies similar to your favourites"
    "</p>",
    unsafe_allow_html=True
)

# LOAD MOVIE DATASET
movies = pd.read_csv("data/movies.csv")

# LOAD RATINGS DATASET
ratings = pd.read_csv("data/ratings.csv")

# CALCULATE AVERAGE RATING FOR EACH MOVIE
average_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()

# RENAME COLUMN
average_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)

# MERGE RATINGS WITH MOVIE DATA
movies = movies.merge(average_ratings, on='movieId', how='left')

# KEEP REQUIRED COLUMNS
movies = movies[['movieId', 'title', 'genres', 'avg_rating']]

# REMOVE NULL VALUES
movies.dropna(inplace=True)

# RESET INDEX
movies.reset_index(drop=True, inplace=True)

# CONVERT GENRES INTO VECTORS
cv = CountVectorizer(tokenizer=lambda x: x.split('|'))

vectors = cv.fit_transform(movies['genres']).toarray()

# CALCULATE COSINE SIMILARITY
similarity = cosine_similarity(vectors)

# TMDB API KEY
API_KEY = st.secrets["TMDB_API_KEY"]

# FETCH POSTER FUNCTION
def fetch_poster(movie_name):

    try:

        clean_name = movie_name.split('(')[0].strip()

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_name}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=30)

        data = response.json()

        if data.get('results') and len(data['results']) > 0:

            for movie in data['results']:

                poster_path = movie.get('poster_path')

                if poster_path:

                    return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:

        print("Poster Error:", e)

        return "https://via.placeholder.com/300x450?text=Error"


# RECOMMENDATION FUNCTION
def recommend(movie):

    movie = movie.lower()

    matching_movies = movies[movies['title'].str.lower().str.contains(movie)]

    if matching_movies.empty:
        return None

    movie_title = matching_movies.iloc[0]['title']

    movie_index = movies[movies['title'] == movie_title].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    similarity_scores = []
    movie_ratings = []

    for i in movie_list:

        movie_name = movies.iloc[i[0]].title

        recommended_movies.append(movie_name)

        similarity_scores.append(round(i[1], 2))

        # GET AVERAGE MOVIE RATING
        rating = movies.iloc[i[0]]['avg_rating']

        movie_ratings.append(round(rating, 1))

        poster = fetch_poster(movie_name)

        time.sleep(1)

        recommended_posters.append(poster)

    searched_movie_poster = fetch_poster(movie_title)

    return (
        movie_title,
        searched_movie_poster,
        recommended_movies,
        recommended_posters,
        similarity_scores,
        movie_ratings
    )


# SEARCH BOX
movie_name = st.text_input(
    "Search Movie",
    placeholder="Enter movie name..."
)

# RECOMMEND BUTTON
if st.button("Recommend Movies"):

    with st.spinner("Finding best recommendations for you..."):

        result = recommend(movie_name)

    if result is None:

        st.error("Movie not found in dataset")

    else:

        (
            searched_movie,
            searched_poster,
            names,
            posters,
            scores,
            ratings
        ) = result

        st.markdown("---")

        # SEARCHED MOVIE SECTION
        st.subheader(" Searched Movie")

        col1, col2 = st.columns([1, 2])

        with col1:

            st.image(searched_poster, width=250)

        with col2:

            st.markdown(f"## {searched_movie}")

            st.write("### Similar movies recommended using cosine similarity")

        st.markdown("---")

        # RECOMMENDATION SECTION
        st.subheader("Top Recommended Movies")

        cols = st.columns(5)

        for idx in range(len(names)):

            with cols[idx]:

                st.image(posters[idx])

                st.markdown(
                    f"<div class='movie-title'>{names[idx]}</div>",
                    unsafe_allow_html=True
                )

                st.write(f"⭐ Rating: {ratings[idx]}/5")
                st.write(f"Similarity: {scores[idx]}")