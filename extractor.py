import re

ROLE_KEYWORDS = [
    "CEO", "CTO", "CFO", "COO", "CIO", "CMO", "CHRO", "Founder", "Co-Founder",
    "Chief [A-Za-z ]+", "Managing Director", "Director", "VP", "Vice President",
    "Product Manager", "Engineering Manager", "Software Engineer", "Developer",
    "Data Scientist", "Marketing Manager", "Account Executive", "Sales", "Recruiter",
    "HR", "Support Engineer", "Technical Support", "Legal Counsel"
]

ROLE_PATTERN = "|".join(ROLE_KEYWORDS)
EXTRACTION_PATTERN = re.compile(
    rf"([A-Z][a-z]+(?:\\s[A-Z][a-z]+)+).{{0,40}}?\\b({ROLE_PATTERN})\\b",
    re.IGNORECASE
)

def extract_employees(text):
    matches = EXTRACTION_PATTERN.findall(text)
    return [
        {"Name": name.strip(), "Title": title.strip()} for name, title in matches
    ]

# File: crawler.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from playwright.sync_api import sync_playwright

visited = set()

def is_internal(base_url, link):
    base = tldextract.extract(base_url)
    link = tldextract.extract(link)
    return base.domain == link.domain or link.domain == ""

def get_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=15000)
        html = page.content()
        browser.close()
    return html

def crawl(url, depth, max_depth):
    if depth > max_depth or url in visited:
        return []
    visited.add(url)
    html = get_page_content(url)
    soup = BeautifulSoup(html, "html.parser")
    links = [url]
    for a in soup.find_all("a", href=True):
        full_url = urljoin(url, a['href'])
        if is_internal(url, full_url):
            links.extend(crawl(full_url, depth+1, max_depth))
    return list(set(links))
