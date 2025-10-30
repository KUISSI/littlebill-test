from fastapi import APIRouter, HTTPException
import httpx
from base64 import b64encode
import os 
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

EMAIL = os.getenv("HIBOUTIK_EMAIL")
API_KEY = os.getenv("HIBOUTIK_API_KEY")
HIBOUTIK_BASE_URL = os.getenv("HIBOUTIK_BASE_URL")

def get_auth_header():
    credentials = f"{EMAIL}:{API_KEY}"
    encoded = b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


@router.get("/customers/search")
async def search_customers(query: str):
    headers = get_auth_header()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{HIBOUTIK_BASE_URL}customers/", headers=headers)
            print(response.text)
            response.raise_for_status()
            customers = response.json()

            
            filtered = [
                {
                    "first_name": customer.get("first_name", ""),
                    "last_name": customer.get("last_name", "")
                }
                for customer in customers
                if query.lower() in customer.get("first_name", "").lower()
                or query.lower() in customer.get("last_name", "").lower()
            ]


            
            return filtered

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))