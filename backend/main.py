from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as customer_router

from app.database import Base, engine
from backend.app.hiboutik_sync import sync_customers




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)

Base.metadata.create_all(bind=engine)

# Synchronisation automatique au démarrage
@app.on_event("startup")
def startup_event():
    print("Synchronisation Hiboutik → sqli.db en cours ...")
    sync_customers()
    print("Synchronisation Hiboutik terminée.")