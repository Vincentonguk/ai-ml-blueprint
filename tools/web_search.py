import requests
from bs4 import BeautifulSoup


def web_search(query: str, max_results: int = 5) -> list[str]:
    """
    Busca no DuckDuckGo e retorna trechos de texto reais da internet.
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "lxml")

    results = []

    for result in soup.select(".result__snippet"):
        text = result.get_text(strip=True)
        if text:
            results.append(text)

        if len(results) >= max_results:
            break

    if not results:
        results.append("Nenhuma informação relevante encontrada na web.")

    return results
