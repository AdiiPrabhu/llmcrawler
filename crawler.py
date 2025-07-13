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
    from playwright.sync_api import TimeoutError
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        try:
            # Increased timeout and added wait_until to improve reliability
            page.goto(url, timeout=30000, wait_until="load")
            html = page.content()
        except TimeoutError:
            print(f"❌ Timeout loading {url}")
            html = ""
        except Exception as e:
            print(f"❌ Error loading {url}: {e}")
            html = ""
        finally:
            browser.close()
        return html


def crawl(url, depth, max_depth, max_pages, count=[0]):
    if depth > max_depth or url in visited or count[0] >= max_pages:
        return []

    visited.add(url)
    count[0] += 1  # Track how many pages have been visited

    html = get_page_content(url)
    soup = BeautifulSoup(html, "html.parser")
    links = [url]

    for a in soup.find_all("a", href=True):
        full_url = urljoin(url, a['href'])
        if is_internal(url, full_url):
            links.extend(crawl(full_url, depth + 1, max_depth, max_pages, count))
            if count[0] >= max_pages:
                break

    return list(set(links))

