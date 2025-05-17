from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import model_validator

#définition d'un modèle pour vérifier qu'une dictionnaire contient une seule clé
class SingleKeyDict(BaseModel):
    __root__ : dict #root est un champ créé permettant de stocker une "value" passée au modèle

    @model_validator(mode="before")
    def check_single_key(cls, value) :
        if len(value) != 1:
            raise ValueError("Le dictionnaire doit contenir une seule clé.")

#définition d'un modèle de donnéees
class yt_data(BaseModel):
    video_type: str = Field(description="Type de vidéo")
    video_url: str = Field(description="URL de la vidéo")
    description_tone: str = Field(description="Ton de la description")
    optional_keywords: str = Field(description="Mots clés optionnels")
    transcript_format: str = Field(description="Format de la transcription")
    transcript: str = Field(description="Transcription de la vidéo")
    languages: List[str] = Field(description="Langues disponibles")
    translation: str = Field(description="Langue de traduction")
    hashtags: str = Field(description="Hashtags à inclure")
    timestamps_mode: str = Field(description="Mode des timestamps")
    manual_timestamps: str = Field(description="Timestamps manuels")
    useful_links: List[SingleKeyDict] = Field(description="Liens utiles")

    

#validation personnalisée 
@model_validator(mode="before")

app = FastAPI()

@app.post("/generate_description")
async def root():
     

