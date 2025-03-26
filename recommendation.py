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
MODEL_PATH = "static/recommendation_model.pkl"


def download_from_s3(bucket_name, s3_key, local_path):
    """Download model from S3 if not available locally"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    if not os.path.exists(local_path):
        try:
            s3.download_file(bucket_name, s3_key, local_path)
            print(f"Model downloaded from S3 and saved to {local_path}")
        except Exception as e:
            raise Exception(f"Error downloading model from S3: {e}")


# Check if model exists locally, else download from S3
download_from_s3(S3_BUCKET_NAME, "recommendation_model.pkl", MODEL_PATH)

# Load the model
with open(MODEL_PATH, "rb") as f:
    combined_model = pickle.load(f)

# Access individual components
cosine_sim = combined_model["cosine_sim"]
indices = combined_model["indices"]
df2 = combined_model["df2"]

# Recommendation function
def get_recommendations(title: str):
    if title not in indices:
        raise HTTPException(status_code=404, detail="Movie not found")

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]

    return df2['title'].iloc[movie_indices].tolist()
