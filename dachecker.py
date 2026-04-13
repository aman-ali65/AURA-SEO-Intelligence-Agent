import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("RAPIDAPI_KEY")
host = os.getenv("RAPIDAPI_HOST")

def get_domain_metrics(domain: str):
    """Fetch DA, PA, and spam score from Moz API via RapidAPI."""
    try:
        url = "https://moz-da-pa1.p.rapidapi.com/v1/getDaPa"
        payload = {"q": domain.replace("https://", "").replace("http://", "").split("/")[0]}
        headers = {
            "x-rapidapi-key": api,
            "x-rapidapi-host": host,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()

        # Add timestamp for logging/debugging
        data["checked_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Cleaned response
        return {
            "domain_authority": data.get("domain_authority", -1),
            "page_authority": data.get("page_authority", -1),
            "spam_score": data.get("spam_score", -1),
            "external_urls_to_url": data.get("external_urls_to_url", -1),
            "external_nofollow_urls_to_url": data.get("external_nofollow_urls_to_url", -1),
            "checked_at": data["checked_at"]
        }

    except Exception as e:
        return {"error": str(e)}

