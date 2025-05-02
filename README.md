
# 🎬 Movie Recommender

This project is a web-based application built using **FastAPI** that recommends similar movies based on user input. It leverages natural language processing and cosine similarity to suggest content-based or collaborative filtering movie recommendations. A clean, interactive web interface allows users to explore similar movies with ease.

## 🌟 Features

- **Search Movies**: Enter a movie name and receive a list of similar titles.
- **Content-Based Filtering**: Uses TF-IDF vectorization and cosine similarity.
- **Collaborative Filtering**: Uses sparse matrix and cosine similarity.
- **TMDB Integration**: Optionally integrates with The Movie Database (TMDb) API to fetch top movies of the day.
- **FastAPI Backend**: High-performance backend built with FastAPI.
- **AWS Integration**: Used AWS S3 storage for storing recommendation models on cloud and retreiving it using AWS IAM user.
- **Simple Frontend**: HTML templates rendered via Jinja2.

## 🗂 Project Structure

```
movie-recommender/
├── main.py                # FastAPI entry point
├── index.py               # UI routes and search handling
├── recommendation.py      # Recommendation logic
├── model.py               # Loads vectorizer and similarity matrix
├── reco_pkl.py            # Handles loading pickled models/data from AWS console.
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (e.g., TMDB API key)
├── templates/             # HTML templates
├── static/                # Static assets (CSS, images)
└── .git/                  # Git version control files
```

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender/python - Copy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables

Create a `.env` file in the project root:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

You can get a free API key from [The Movie Database](https://www.themoviedb.org/documentation/api).

### 6. Run the Application

```bash
python index.py
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🚀 Usage

1. Launch the app and open it in your browser.
2. Enter a movie name into the search field.
3. Select which type of recommendation you want ( Content Based or Collaborative filtering)
4. View recommended similar movies.
5. (Optional) See top movies of the day fetched from TMDB.

## 🔍 Dependencies

- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Jinja2
- python-dotenv

All required packages are listed in `requirements.txt`.

## 📷 Demo
![1-Home](https://github.com/user-attachments/assets/0dcbb22d-c312-4167-9b37-5fab4215b592)
![2-Recommend](https://github.com/user-attachments/assets/32f0e79d-a10a-4d31-82b3-bc7b7f18204e)
![3-Collaborative Filtering](https://github.com/user-attachments/assets/bf5570d9-4679-406a-a795-f327ad168941)
![4-Content Based Filtering](https://github.com/user-attachments/assets/28474377-c17d-48e1-b6ee-18dc9f69e375)
![5-About Dataset](https://github.com/user-attachments/assets/1cca05d2-768c-4abe-88db-fbc97597b59e)
![6-EDA](https://github.com/user-attachments/assets/3fb6eeff-3b1b-414a-9998-342f18669ce5)

## 📄 Deployement
This app is deployed using render service.
Visit : https://movie-recc-30m.onrender.com
