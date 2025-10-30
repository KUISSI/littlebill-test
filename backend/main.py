from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.hiboutik_customer import router as customer_router
app = FastAPI()

# Middleware CORS pour autoriser toutes les origines (pratique en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod, précise tes origines !
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du router pour les routes /customers/
app.include_router(customer_router)