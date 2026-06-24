from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from recommend import recommend_music

import numpy as np
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = load_model(
    "model/MobileNetV2_Valence_Arousal_v2.keras"
)
def predict_emotion(image_path):

    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img)
    img = preprocess_input(
        img.astype(np.float32)
    )
    img = np.expand_dims(
        img,
        axis=0
    )
    prediction = model.predict(
        img,
        verbose=0
    )
    valence = float(
        prediction[0][0][0]
    )
    arousal = float(
        prediction[1][0][0]
    )
    return valence, arousal


@app.get("/")
def root():
    return {
        "message": "Musify API Running"
    }

@app.post("/recommend")
async def recommend(
    file: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:

        temp_file.write(
            await file.read()
        )
        temp_path = temp_file.name
    # output model (0-1)
    valence_raw, arousal_raw = predict_emotion(
        temp_path
    )
    # convert ke -1 sampai 1
    valence = (
        valence_raw * 2
    ) - 1
    arousal = (
        arousal_raw * 2
    ) - 1
    songs = recommend_music(
        valence,
        arousal,
        top_n=10
    )
    return {
        "valence": round(valence,3),
        "arousal": round(arousal,3),
        "songs": songs
    }