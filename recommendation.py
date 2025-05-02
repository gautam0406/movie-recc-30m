import pickle
import pandas as pd
from fastapi import HTTPException
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

CBF_PATH = "static/recommendation_model.pkl"
CF_PATH = "static/recommendation_model_CF.pkl"


def download_from_s3(bucket_name, s3_key, local_path):
    """Download model from S3 only if not available locally or corrupted"""
    if os.path.exists(local_path):
        print(f"Model already exists locally at {local_path}. Skipping download.")
        return
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.download_file(bucket_name, s3_key, local_path)
        print(f"Model downloaded from S3 and saved to {local_path}")
    except Exception as e:
        raise Exception(f"Error downloading model from S3: {e}")
    


def load_selected_model(model_type: str):
    """Load the selected model dynamically"""
    if model_type.lower() == "cbf":
        model_path = CBF_PATH
        s3_key = "recommendation_model.pkl"
    elif model_type.lower() == "cf":
        model_path = CF_PATH
        s3_key = "recommendation_model_CF.pkl"
    else:
        raise HTTPException(status_code=400, detail="Invalid model type. Choose 'cbf' or 'cf'.")

    # Download model if not available locally
    download_from_s3(S3_BUCKET_NAME, s3_key, model_path)

    # Load the selected model
    with open(model_path, "rb") as f:
        selected_model = pickle.load(f)
    
    print(f"{model_type.upper()} Model loaded successfully!")
    return selected_model

# Recommendation function
def get_recommendations_CBF(title: str, selected_model):
    cosine_sim = selected_model["cosine_sim"]
    indices = selected_model["indices"]
    df2 = selected_model["df2"]

    title = title.lower()

    if title not in indices:
        raise HTTPException(status_code=404, detail="Movie not found")

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]

    return df2['title'].iloc[movie_indices].tolist()

# def get_recommendations_CF(title: str, selected_model):
#     similarity_matrix = selected_model["similarity_matrix"]
#     movie_titles = selected_model["movie_titles"]

#     if title not in similarity_matrix.columns:
#         return f"Movie '{title}' not found in the dataset."
    
#     # Get similarity scores for the selected movie
#     sim_scores = similarity_matrix[title].sort_values(ascending=False)
    
#     # Get top N most similar movies (excluding the movie itself)
#     top_similar_movies = sim_scores.iloc[1:11]
#     recommended_movies = pd.DataFrame({'title': top_similar_movies.index, 'similarity_score': top_similar_movies.values})
    
#     # Return movie recommendations with similarity scores
#     return recommended_movies

# def get_recommendations_CF(title: str, selected_model):
#     # Load similarity matrix from the model
#     similarity_matrix = selected_model["similarity_matrix"]

#     # Check if the title exists in the dataset
#     if title not in similarity_matrix.columns:
#         raise HTTPException(status_code=404, detail=f"Movie '{title}' not found in the dataset.")
    
#     # Get similarity scores for the selected movie
#     sim_scores = similarity_matrix[title].sort_values(ascending=False)
    
#     # Get top 10 most similar movies (excluding the movie itself)
#     top_similar_movies = sim_scores.iloc[1:11]
    
#     # Return only the movie titles as a list
#     recommended_movies = top_similar_movies.index.tolist()
    
#     return recommended_movies

def get_recommendations_CF(title: str, selected_model):

    # Get similarity matrix from the model
    similarity_matrix = selected_model["similarity_matrix"]
    interaction_df = selected_model["interaction_df"]

    title = title.lower()

    movie_id = interaction_df[interaction_df['title'] == title]['id'].values

    if len(movie_id) == 0:
        raise HTTPException(status_code=404, detail="Movie not found")   
    
    movie_id = movie_id[0]

    if movie_id not in similarity_matrix.index:
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found in the dataset.")

    
    # Get similarity scores for the selected movie
    sim_scores = similarity_matrix.loc[movie_id].sort_values(ascending=False)
    
    # Get top 10 most similar movies (excluding the movie itself)
    top_similar_movies = sim_scores.iloc[1:11]
    
    # Return movie titles as a list
    # recommended_movies = top_similar_movies.index.tolist()
    recommended_movies = interaction_df[interaction_df['id'].isin(top_similar_movies.index)]['title'].tolist()

    
    return recommended_movies
