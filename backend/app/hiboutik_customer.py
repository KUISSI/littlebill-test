from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

class Customer(BaseModel):
    nom: str
    prenom: str

HIBOUTIK_USER = os.getenv("HIBOUTIK_USER")
HIBOUTIK_PASSWORD = os.getenv("HIBOUTIK_PASSWORD")

@router.get("/customers/", response_model=List[Customer])
def get_customers(
    nom: Optional[str] = Query(None, description="Nom du customer à rechercher"),
    prenom: Optional[str] = Query(None, description="Prénom du customer à rechercher")
):
    if not HIBOUTIK_USER or not HIBOUTIK_PASSWORD:
        raise HTTPException(status_code=500, detail="Identifiants Hiboutik non configurés.")

    url = "https://techtest.hiboutik.com/api/customers/search"
    credentials = f"{HIBOUTIK_USER}:{HIBOUTIK_PASSWORD}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_credentials}",
        "Accept": "application/json"
    }
    params = {}
    if nom:
        params["last_name"] = nom
    if prenom:
        params["first_name"] = prenom

    if not params:
        raise HTTPException(status_code=400, detail="Veuillez préciser au moins un nom ou un prénom.")

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erreur Hiboutik: " + response.text)
        hiboutik_customers = response.json()
        return [
            Customer(
                nom=c.get("last_name", ""),
                prenom=c.get("first_name", ""),
            )
            for c in hiboutik_customers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))