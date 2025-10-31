from fastapi import APIRouter, Query, HTTPException, Path
from typing import Any, List, Optional
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
    customers_id: int

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
                customers_id=c.get("customers_id", 0)
            )
            for c in hiboutik_customers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer/{customers_id}/sales", response_model=List[Any])
def get_sales_for_customer(
    customers_id: int = Path(..., description="ID du client"),
    hiboutik_p: Optional[int] = Query(1, description="Page Hiboutik (250 résultats/page)"),
    page: int = Query(1, description="Page locale par tranche de 5 ventes")
):
    """
    Retourne la liste des ventes pour un client donné, paginée par 5 (pagination locale).
    """
    if not HIBOUTIK_USER or not HIBOUTIK_PASSWORD:
        raise HTTPException(status_code=500, detail="Identifiants Hiboutik non configurés.")

    url = f"https://techtest.hiboutik.com/api/customer/{customers_id}/sales"
    credentials = f"{HIBOUTIK_USER}:{HIBOUTIK_PASSWORD}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_credentials}",
        "Accept": "application/json"
    }
    params = {"p": hiboutik_p}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Client ou ventes non trouvés.")
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Authentification Hiboutik invalide.")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erreur Hiboutik: " + response.text)
        hiboutik_sales = response.json()
        # Pagination locale par tranche de 5
        local_page_size = 5
        start = (page - 1) * local_page_size
        end = start + local_page_size
        return hiboutik_sales[start:end]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
    

@router.get("/customer/{customers_id}/sales", response_model=List[Any])
def get_sales_for_customer(
    customers_id: int = Path(..., description="ID du client"),
    hiboutik_p: Optional[int] = Query(1, description="Page Hiboutik (250 résultats/page)"),
    page: int = Query(1, description="Page locale par tranche de 5 ventes")
):
    """
    Retourne la liste des ventes pour un client donné, paginée par 5 (pagination locale).
    """
    if not HIBOUTIK_USER or not HIBOUTIK_PASSWORD:
        raise HTTPException(status_code=500, detail="Identifiants Hiboutik non configurés.")

    url = f"https://techtest.hiboutik.com/api/customer/{customers_id}/sales"
    credentials = f"{HIBOUTIK_USER}:{HIBOUTIK_PASSWORD}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_credentials}",
        "Accept": "application/json"
    }
    params = {"p": hiboutik_p}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Client ou ventes non trouvés.")
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Authentification Hiboutik invalide.")
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erreur Hiboutik: " + response.text)
        hiboutik_sales = response.json()
        # Pagination locale par tranche de 5
        local_page_size = 5
        start = (page - 1) * local_page_size
        end = start + local_page_size
        return hiboutik_sales[start:end]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))