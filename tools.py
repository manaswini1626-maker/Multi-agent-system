from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from rich import print
from ddgs import DDGS

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web and return titles, URLs and snippets."""
    results = DDGS().text(query, max_results=3)
    return "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}"
        for r in results
    )

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


if __name__ == "__main__":
    print(web_search.invoke("What are the recent news of war?"))
    print(scrape_url.invoke("https://example.com"))