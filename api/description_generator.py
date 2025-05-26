from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain_together import ChatTogether
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator
from typing import List
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import os


llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    temperature=1,
    max_tokens=1300,
    api_key=os.getenv("TOGETHER_API_KEY"),
)

#définition d'une structure de données
class yt_description(BaseModel):
    title: str = Field(description="video description title")
    resume: str = Field(description="video description resume")
    links: List[dict] = Field(description="video description links")
    timestamps: str = Field(description="video description timestamps")
    keywords: str = Field(description="video description keywords")
    call_to_action: str = Field(description="video description hashtags")
    about_channel: str = Field(description="video description about channel")


    @field_validator("keywords")
    @classmethod
    def keywords_must_be_list(cls, field):
        if not isinstance(field, str) or "," not in field:
            raise ValueError("Les mots clés doivent être séparés par des virgules et être une string.")
        return field


def process_video(data):

    if data["timestamps_mode"] == "manuel":
        timestamps_instruction = f"Utiliser ces timestamps : {data['manual_timestamps']}"
    else:
        timestamps_instruction = """
🔥 TIMESTAMPS TRANSITIONS ULTRA-PRÉCIS - RÈGLES STRICTES :

1. DÉTECTION OBLIGATOIRE DES :
   - Marqueurs explicites : 
     "Passons à...", "Maintenant voyons...", "2ème point...", 
     "Problème :", "Solution :", "Mais attention...", 
     "La question est...", "En réalité..."
   - Changements de tonalité (ex: passage théorique → démo)
   - Alternances claires (thèse → antithèse, problème → solution)

2. FORMAT FERMÉ :
[MM:SS] - [Verbe d'action] [Sujet] 
Exemples VALIDES :
00:00 - Intro
02:15 - Deuxième point, étape , sujet
04:30 - Troisième point, étape , sujet
07:00 - Quatrième point, étape , sujet
09:45 - Cinquième point, étape , sujet

3. INTERDITS :
- Pas de timestamps sans transition audible
- Pas de descriptions > 4 mots
- Pas de résumés de contenu

"""

    data["timestamps_instruction"] = timestamps_instruction

    # Chargement de la transcription
    try:
        loader = YoutubeLoader.from_youtube_url(
            data['video_url'],
            add_video_info=False,
            transcript_format=TranscriptFormat.CHUNKS,
            chunk_size_seconds=4,
            language=["fr", "id"],
            translation="fr",
        )
        docs = loader.load()
    except (TranscriptsDisabled, NoTranscriptFound, Exception) as e:
        return {"error": f"Impossible de récupérer la transcription : {str(e)}"}

    # Nettoyage de la sortie pour garder uniquement les timecodes et le texte
    transcript = "\n".join([f"{chunk.page_content} - {chunk.metadata['start_timestamp']}" for chunk in docs])
    data['transcript'] = transcript

    #création d'un parseur de données
    parser = PydanticOutputParser(pydantic_object=yt_description)

    # Définition du prompt
    prompt = PromptTemplate(
        input_variables=[
            "video_type",
            "video_url",
            "description_tone",
            "optional_keywords",
            "transcript_format",
            "transcript",
            "languages",
            "translation",
            "hashtags",
            "timestamps_mode",
            "timestamps_instruction",
            "useful_links",
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""
Tu es un expert YouTube et spécialiste SEO.

Ta mission est de produire une description de vidéo YouTube optimisée pour :
- attirer l’attention dès les premières secondes
- booster le SEO avec les bons mots-clés et hashtags
- encourager les likes, commentaires et abonnements
- s’adapter au type de vidéo ({video_type}) et au ton demandé ({description_tone})

Tu dois t’appuyer sur :
- la transcription suivante au format {transcript_format} : {transcript}
- la langue principale : {languages}
- la traduction éventuelle : {translation}
- les mots-clés supplémentaires (optionnels) : {optional_keywords}
- les hashtags suggérés : {hashtags}
- les indications pour le chapitrage : {timestamps_instruction}
- les liens utiles fournis : {useful_links}

---

🎯 **Consignes de sortie** :
Ne retourne rien d'autre que ce JSON avec les champs suivants :
1. "title" (1–2 phrases)
   → Adresse-toi directement au spectateur en utilisant un ton {description_tone}.
   **Exemple** :
   Tu veux découvrir comment j'ai transformé ma routine quotidienne pour booster ma productivité ? Regarde cette vidéo jusqu'au bout !

2. "resume"
   → Résume en quelques phrases ce que le spectateur va apprendre ou découvrir dans la vidéo. Sois personnel et engageant.
   **Exemple** :
   Dans cette vidéo, je partage avec toi mes astuces pour organiser efficacement ta journée et atteindre tes objectifs plus rapidement.

3. "links" (liste avec titre + lien) à partir des données d'entrée. Utilise les liens fournis dans la variable {useful_links} sous ce format :
   Exemple :
   🔗 Liens utiles
   Mon planner préféré : https://monplanner.com
   Application de gestion du temps : https://gestiondutemps.app

4. "timestamps"
   → Génére une section chapitrée en texte (pas en tableau), suivant les consignes suivantes : {timestamps_instruction}
   Utilise le mode de timestamps : {timestamps_mode}
   **Exemple** :
   ⏱️Chapitrages :
   00:00 – Introduction
   01:30 – Astuce n°1 : Planification
   03:45 – Astuce n°2 : Gestion du temps
   06:10 – Astuce n°3 : Élimination des distractions
   08:25 – Conclusion

5.  "keywords"
   → Intègre les mots-clés ({optional_keywords}) et hashtags ({hashtags}) de manière naturelle dans la description.
   **Exemple** :
   Mots-clés : productivité, organisation, gestion du temps
   #Productivité #Organisation #GestionDuTemps

6. "call_to_action"
   → Encourage le spectateur à liker, commenter, s’abonner et partager la vidéo.
   **Exemple** :
   Si tu as aimé cette vidéo, n'oublie pas de liker 👍, de t'abonner 🔔 et de partager avec tes amis ! Dis-moi en commentaire quelle astuce tu vas essayer en premier.

7. "about_channel"
   → Ajoute une brève présentation de la chaîne et invite à explorer d’autres contenus.

---

Tu peux t’inspirer du style de description utilisé par les meilleurs créateurs de contenu YouTube dans ta thématique. Rends chaque section fluide, humaine et cohérente.

 L’objectif est de produire une description complète, engageante et parfaitement optimisée à partir de la vidéo suivante : {video_url}

N'oublie pas d'utiliser des **pronoms personnels** ("je", "tu", "nous") pour créer une relation directe avec le spectateur.

""",

    )

    # Formatage du prompt
    #formatted_prompt = prompt.format(**data_test)

    # Passage de la requête au LLM
    #response = llm.invoke([("human", formatted_prompt)])
    #return response.content

    #création d'une chain
    chain = prompt | llm | parser
    result = chain.invoke(data)
    return result

