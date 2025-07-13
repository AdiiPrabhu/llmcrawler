# File: main.py
from crawler import crawl, get_page_content
from bs4 import BeautifulSoup
from llm_agent import extract_employees_from_llm_chunked
from utils import save_data

def extract_all(seed_url, depth, max_pages=20):
    results = []
    all_links = crawl(seed_url, 0, depth, max_pages)
    for link in all_links:
        try:
            html = get_page_content(link)
            if not html.strip():
                continue

            # Extract only the visible content inside <body>
            soup = BeautifulSoup(html, "html.parser")
            body = soup.body
            if body:
                text = body.get_text(separator=" ", strip=True)
            else:
                text = html  # fallback in case <body> is missing

            employees = extract_employees_from_llm_chunked(text)
            for emp in employees:
                emp["Source URL"] = link
            results += employees

        except Exception as e:
            print(f"Error on {link}:", e)
    return results
