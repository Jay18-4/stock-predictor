# storage.py
import os
import io
import pandas as pd
import boto3

# Environment variables
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")  # e.g., https://<account>.r2.cloudflarestorage.com

# Initialize the client
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

def read_csv(file_name: str) -> pd.DataFrame:
    """Download CSV from R2 and return as DataFrame."""
    try:
        obj = s3.get_object(Bucket=R2_BUCKET_NAME, Key=file_name)
        return pd.read_csv(io.StringIO(obj['Body'].read().decode('utf-8')))
    except s3.exceptions.NoSuchKey:
        print(f"[WARN] File {file_name} not found in bucket. Returning empty DataFrame.")
        return pd.DataFrame()

def write_csv(df: pd.DataFrame, file_name: str):
    """Upload DataFrame to R2 as CSV."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=R2_BUCKET_NAME, Key=file_name, Body=csv_buffer.getvalue())
    print(f"[INFO] File {file_name} uploaded to R2 bucket {R2_BUCKET_NAME}.")
