# 🎬 Movie Recommendation System

A content-based movie recommendation system built using **Python, Streamlit, and Machine Learning**. The system recommends similar movies based on their genres using **CountVectorizer** and **Cosine Similarity**.

## 📌 Project Overview

This project allows users to search for a movie and receive the **top 5 similar movie recommendations**.

The recommendation system analyzes movie genres, converts them into numerical vectors, and calculates the similarity between movies using cosine similarity.

Movie posters are fetched using the **TMDB API**.

## 🚀 Features

* 🔎 Search for a movie
* 🎯 Get the top 5 similar movie recommendations
* 🤖 Content-based recommendation
* 📊 Cosine similarity-based movie matching
* 🎬 Movie posters using TMDB API
* 🖥️ Interactive Streamlit web interface
* ⭐ Similarity score for recommended movies

## 🧠 How It Works

The system follows these steps:

1. Movie data is loaded from the MovieLens dataset.
2. Movie titles and genres are selected from the dataset.
3. Movie genres are converted into numerical vectors using `CountVectorizer`.
4. Cosine similarity is calculated between all movies.
5. When the user searches for a movie, the system finds the matching movie.
6. The similarity scores are compared with other movies.
7. The top 5 most similar movies are displayed.
8. Movie posters are fetched using the TMDB API.

### Recommendation Flow

```text
Movie Dataset
      ↓
Select Movie Title & Genres
      ↓
CountVectorizer
      ↓
Genre Vectors
      ↓
Cosine Similarity
      ↓
Find Similar Movies
      ↓
Top 5 Recommendations
      ↓
Display Movie Posters
```

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data handling
* **Scikit-learn** – Machine learning and cosine similarity
* **Streamlit** – Web application
* **Requests** – API requests
* **TMDB API** – Movie poster data

## 📂 Project Structure

```text
movie-recommendation-system/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   └── movies.csv
│
└── .streamlit/
    └── secrets.toml
```

> `secrets.toml` contains the TMDB API key and is excluded from GitHub using `.gitignore`.

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the project folder

```bash
cd movie-recommendation-system
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Configure the TMDB API key

Create the following file:

```text
.streamlit/secrets.toml
```

Add:

```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## 🖥️ Application Preview

The application provides a simple interface where users can enter a movie name and receive similar movie recommendations along with movie posters and similarity scores.

## 🔮 Future Improvements

* Improve movie search and matching
* Add movie ratings and popularity
* Include additional movie features such as cast, directors, and keywords
* Improve recommendation accuracy
* Add collaborative filtering
* Deploy the application online
* Add a more advanced recommendation model

## 👨‍💻 Author

 RAKSHAN R ADAPA

Robotics and Artificial Intelligence Engineering Student
