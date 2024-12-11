from fastapi import FastAPI, HTTPException
import requests 
import subprocess
import os
from contextlib import asynccontextmanager
import asyncio
import threading
from app.train import train_single_model, INDEX_TO_SPECIES

def server_process():
        return subprocess.Popen(["mlflow", "server", "--host", "127.0.0.1", "--port", os.environ['SERVER_PORT']])

def model_process(): 
        return subprocess.Popen(["mlflow", "models", "serve", "-m", os.environ['MODEL_URI'], "--host", "127.0.0.1", "--port", os.environ['MODEL_PORT'], "--no-conda"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    sp = server_process()
    train_single_model()
    mp = model_process()
    yield
    sp.kill()
    mp.kill()
    
app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(sepal_length: float,sepal_width: float, petal_length: float, petal_width: float):

    try:
        data = {"inputs":
        [
            [sepal_length, sepal_width, petal_length, petal_width]
        ]}
        response = requests.post(f'http://127.0.0.1:{os.environ["MODEL_PORT"]}/invocations', json=data)
        if response.status_code == 200:
            predictions = response.json()['predictions'][0]
            predictions = INDEX_TO_SPECIES[predictions]
            return {'prediction': predictions}
        
        else: 
            raise HTTPException(status_code=500)
    
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

