from fastapi import FastAPI,Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from recommendation import load_selected_model,get_recommendations_CF,get_recommendations_CBF
# from recommendation import get_recommendations
import requests
import os
from dotenv import load_dotenv
import time



app = FastAPI()

# Mount the "static" folder to serve CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")

#declaring the templates folder
templates = Jinja2Templates(directory="templates")




# Load environment variables from .env file
load_dotenv()

# Fetch API key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is not set. Please set it in the .env file.")

# Function to fetch top movies from TMDb API
def get_top_movies_from_tmdb():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    
    try:
        time.sleep(1)  # Add 1-second delay between requests
        response = requests.get(url)
        data = response.json()

        # Extract relevant movie data
        top_movies = []
        for movie in data.get("results", []):
            top_movies.append({
                "title": movie["title"],
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                "release_date": movie.get("release_date", "N/A"),
                "rating": movie.get("vote_average", 0)
            })

        return top_movies[:10]  # Get top 10 movies
    except Exception as e:
        print(f"Error fetching movies from TMDb: {e}")
        return []


@app.get("/")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

@app.get("/dataset_info")
def description_page(request: Request):
    return templates.TemplateResponse("dataset_info.html", {"request": request})


@app.get("/recommend")
def recommend_page(request: Request):
    top_movies = get_top_movies_from_tmdb()
    return templates.TemplateResponse("recommend.html", {
        "request": request, 
        "recommendations": None,
        "error": None,
        "top_movies": top_movies
    })

@app.post("/recommend")
def get_movie_recommendations(
    request: Request,
    movie_title: str = Form(...),
    filter_type: str = Form(...),  # Added filter type from the form
):
    try:
        # Load the selected model dynamically based on the filter type
        selected_model = load_selected_model(filter_type)

        # Get recommendations using the selected model
        if filter_type == "cf":
            recommendations = get_recommendations_CF(movie_title, selected_model)
        elif filter_type == "cbf":
            recommendations = get_recommendations_CBF(movie_title, selected_model)
        else:
            raise HTTPException(status_code=400, detail="Invalid filter type")

        # Fetch top movies from TMDb API
        top_movies = get_top_movies_from_tmdb()

        return templates.TemplateResponse("recommend.html", {
            "request": request,
            "recommendations": recommendations,
            "movie_title": movie_title,
            "top_movies": top_movies
        })

    except HTTPException as e:
        return templates.TemplateResponse("recommend.html", {
            "request": request,
            "error": e.detail,
            "recommendations": None,
            "top_movies": get_top_movies_from_tmdb()
        })


@app.get("/eda")
def index_page(request: Request):
    return templates.TemplateResponse("eda.html", {"request": request})
