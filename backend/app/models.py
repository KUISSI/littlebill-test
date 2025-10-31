# Tes Pydantic models

from pydantic import BaseModel

class Customer(BaseModel):
    nom: str
    prenom: str
    customers_id: int

