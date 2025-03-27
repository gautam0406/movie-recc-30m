import boto3
from dotenv import load_dotenv
import os
import pickle

# Load environment variables
load_dotenv()

# AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

output_path = "models/recommendation_model.pkl"

def upload_to_s3(file_path, bucket_name, s3_key):
    """Upload a file to S3"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")


def save_model(cosine_sim, indices, df2, output_path):
    combined_model = {
        "cosine_sim": cosine_sim,
        "indices": indices,
        "df2": df2
    }
    with open(output_path, "wb") as f:
        pickle.dump(combined_model, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Model saved successfully as '{output_path}'!")

    # Upload model to S3
    upload_to_s3(output_path, S3_BUCKET_NAME, "recommendation_model.pkl")
