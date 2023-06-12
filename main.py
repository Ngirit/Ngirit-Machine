import os
import uvicorn
import traceback
import tensorflow as tf

from pydantic import BaseModel
from urllib.request import Request
from fastapi import FastAPI, Response, UploadFile
#from utils import load_image_into_numpy_array

app = FastAPI()

def predict():
    predictions = get_predictions(request)

    return jsonify(predictions)
