from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
import time
import secrets

app = FastAPI()

security = HTTPBasic()

# Dummy in-memory database
users = {os.environ["API_USER"]: generate_password_hash(os.environ["API_PASSWORD"])}

# Load the ratings dataset
def _read_ratings(file_path: str) -> pd.DataFrame:
    ratings = pd.read_csv(file_path)
    ratings = ratings.sample(n=100000, random_state=0)
    ratings = ratings.sort_values(by=["timestamp", "userId", "movieId"])
    return ratings

ratings_df = _read_ratings("/ratings.csv")


def verify_password(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
    if username in users and check_password_hash(users.get(username), password):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/")
def read_root():
    return {"message": "Hello from the Movie Rating API!"}


@app.get("/ratings")
def get_ratings(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    credentials: HTTPBasicCredentials = Depends(security),
):
    # Authenticate the user
    verify_password(credentials)

    # Date filtering
    start_date_ts = _date_to_timestamp(start_date)
    end_date_ts = _date_to_timestamp(end_date)

    subset = ratings_df

    if start_date_ts:
        subset = subset.loc[subset["timestamp"] >= start_date_ts]

    if end_date_ts:
        subset = subset.loc[subset["timestamp"] < end_date_ts]

    # Pagination
    subset = subset.iloc[offset : offset + limit]

    return {
        "result": subset.to_dict(orient="records"),
        "offset": offset,
        "limit": limit,
        "total": ratings_df.shape[0],
    }


def _date_to_timestamp(date_str: Optional[str]) -> Optional[int]:
    if date_str is None:
        return None
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d")))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
