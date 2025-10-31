import requests
import base64
import os
from app.database import SessionLocal
from app.models import Customer

HIBOUTIK_USER = os.getenv("HIBOUTIK_USER")
HIBOUTIK_PASSWORD = os.getenv("HIBOUTIK_PASSWORD")
HIBOUTIK_URL = "https://techtest.hiboutik.com/api/customers/search"

def fetch_hiboutik_customers():
    credentials = f"{HIBOUTIK_USER}:{HIBOUTIK_PASSWORD}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_credentials}",
        "Accept": "application/json"
    }
    response = requests.get(HIBOUTIK_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def sync_customers():
    hiboutik_customers = fetch_hiboutik_customers()
    db = SessionLocal()
    for c in hiboutik_customers:
        db_customer = db.query(Customer).filter_by(customers_id=c["customers_id"]).first()
        if db_customer:
            db_customer.nom = c.get("last_name", "")
            db_customer.prenom = c.get("first_name", "")
        else:
            db.add(Customer(
                nom=c.get("last_name", ""),
                prenom=c.get("first_name", ""),
                customers_id=c.get("customers_id")
            ))
    db.commit()
    db.close()

if __name__ == "__main__":
    sync_customers()
    print("Synchronisation terminée !")