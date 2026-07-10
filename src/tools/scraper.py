import requests
from bs4 import BeautifulSoup


URL = "https://www.epassport.gov.bd"


def scrape_data():

    try:

        response = requests.get(URL, timeout=10)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        return {
            "status": True,
            "source": "Website",
            "message": "Website Connected"
        }

    except Exception:

        return {
            "status": False,
            "source": "Local Database",
            "message": "Scraping Failed"
        }