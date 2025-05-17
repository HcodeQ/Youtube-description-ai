from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import model_validator
from typing import List
from description_generator import process_video

#définition d'un modèle pour vérifier qu'une dictionnaire contient une seule clé
class SingleKeyDict(BaseModel):
    __root__ : dict #root est un champ créé permettant de stocker une "value" passée au modèle

    @model_validator(mode="before")
    def check_single_key(cls, value) :
        if len(value) != 1:
            raise ValueError("Le dictionnaire doit contenir une seule clé.")

#définition d'un modèle de donnéees
class VideoData(BaseModel):
    video_type: str
    video_url: str
    description_tone: str
    optional_keywords: str
    transcript_format: str
    transcript: str
    languages: List[str]
    translation: str
    hashtags: str
    timestamps_mode: str
    manual_timestamps: str
    useful_links: List[SingleKeyDict]


app = FastAPI()

@app.post("/generate")
async def generate_description(data: VideoData):
    result = process_video(data)
    return result