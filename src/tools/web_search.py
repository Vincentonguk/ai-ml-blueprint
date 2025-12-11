import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def web_search(query: str, max_results: int = 5) -> list[str]:
    """
    Busca real na internet usando a API da Tavily.
    """

    if not TAVILY_API_KEY:
        return ["❌ ERRO: TAVILY_API_KEY não encontrada no .env"]

    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_answer": True
    }

    try:
        response = requests.post(url, json=payload, timeout=20)

        if response.status_code != 200:
            return [f"❌ Erro Tavily: {response.text}"]

        data = response.json()
        results = []

        for item in data.get("results", []):
            content = item.get("content")
            if content:
                results.append(content)

        return results if results else ["Nenhuma informação encontrada."]

    except Exception as e:
        return [f"❌ Erro inesperado: {e}"]
