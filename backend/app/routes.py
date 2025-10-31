from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import SessionLocal
from app.models import Customer, Sale
from app.schemas import CustomerSchema, SaleSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/customers", response_model=List[CustomerSchema])
def get_customers(nom: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Customer)
    if nom:
        query = query.filter(Customer.nom.ilike(f"%{nom}%"))
    return query.all()

@router.get("/customer/{customers_id}/sales", response_model=List[SaleSchema])
def get_sales_for_customer(customers_id: int, db: Session = Depends(get_db)):
    sales = db.query(Sale).filter(Sale.customer_id == customers_id).all()
    if not sales:
        raise HTTPException(status_code=404, detail="Aucune vente trouvée pour ce client.")
    return sales