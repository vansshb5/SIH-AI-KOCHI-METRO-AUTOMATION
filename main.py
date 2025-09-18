from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS for frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load train.csv
df = pd.read_csv("trains.csv")

@app.get("/fitness/{train_id}")
def get_fitness(train_id: str):
    row = df[df["Train_ID"] == train_id]
    if row.empty:
        return {"error": "Train not found"}
    return row.iloc[0].to_dict()
