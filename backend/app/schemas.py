from pydantic import BaseModel

class CustomerSchema(BaseModel):
    nom: str
    prenom: str
    customers_id: int

    class Config:
        orm_mode = True

class SaleSchema(BaseModel):
    sale_id: int
    date: str
    total: float
    currency: str
    store_id: int
    customer_id: int

    class Config:
        orm_mode = True