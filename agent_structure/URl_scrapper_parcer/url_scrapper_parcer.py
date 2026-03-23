from agent_structure.state import GraphState
from bs4 import BeautifulSoup
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def scrapper_parcer(state: GraphState):
    urls = state["collected_urls"]
    parsed_pages = []

    for item in urls:
        try:
            html_doc = get_doc(item["url"])
            text = parcer(html_doc)
            if len(text) > 200:
                parsed_pages.append({"content": text, "score": item.get("score", 0)})
        except requests.exceptions.SSLError:
            print(f"ADA: SSL error skipping {item['url']}")
        except requests.exceptions.ConnectionError:
            print(f"ADA: Connection error skipping {item['url']}")
        except requests.exceptions.Timeout:
            print(f"ADA: Timeout skipping {item['url']}")
        except Exception as e:
            print(f"ADA: Unexpected error for {item['url']}: {e}")

    print(f"ADA: scraped {len(parsed_pages)} pages from {len(urls)} urls")
    return {"parsed_pages": parsed_pages}


def get_doc(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()  # raises for 403, 404, etc.
    return response.text


def parcer(html_doc: str) -> str:
    soup = BeautifulSoup(html_doc, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.extract()
    text = soup.get_text(separator=" ")
    lines = [line.strip() for line in text.splitlines()]
    return " ".join([line for line in lines if len(line) > 40])