import requests
from typing import List, Dict, Any

class TavilySearch:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"

    def search(self, query: str) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "num_results": 5}
        resp = requests.get(self.base_url, headers=headers, params=params, timeout=20)

        if resp.status_code != 200:
            raise Exception(f"Tavily API Error: {resp.text}")

        data = resp.json()
        return data.get("results", [])
