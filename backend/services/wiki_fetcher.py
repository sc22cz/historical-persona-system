import requests

def fetch_wikipedia_text(name: str) -> str:
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_")
    
    headers = {"User-Agent": "HistoricalPersonaSystem/1.0"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    return data.get("extract", None)