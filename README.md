# LLM-Powered Employee Data Extractor

An intelligent agent that recursively crawls a company website, uses GPT-4 to identify team or employee-related pages, and extracts structured employee data like name, title, and location.

## Features

- Recursive web crawler with depth + page limits
- GPT-4 powered employee data extractor (name, title, location)
- Outputs to CSV or JSON
- Streamlit UI for interactive usage
- Supports JavaScript-heavy websites using Playwright
- Dockerized for reliable deployment
- Deployable on Fly.io with Chromium support

## Tech Stack

| Component    | Tool/Library              |
|--------------|---------------------------|
| Frontend     | Streamlit                 |
| LLM Engine   | OpenAI GPT-4 (LangChain)  |
| Crawler      | Playwright + BeautifulSoup|
| Export       | Pandas / JSON             |
| Deployment   | Docker + Fly.io           |

## Project Structure

```
llm-employee-extractor/
├── ui_app.py         # Streamlit frontend
├── main.py           # Pipeline controller
├── llm_agent.py      # GPT-based extractor (chunked)
├── crawler.py        # Playwright-based link explorer
├── utils.py          # File writer (CSV/JSON)
├── requirements.txt  # All Python deps
├── Dockerfile        # For Fly.io or local Docker
├── fly.toml          # Fly.io deployment config
└── .env              # API keys (not committed)
```

## How It Works

1. Input a seed URL via UI
2. Recursively crawls internal pages (up to N pages, depth D)
3. Renders each page with Playwright
4. Extracts text from the <body> tag
5. Splits body text into overlapping chunks
6. Sends each chunk to GPT-4 using a structured prompt
7. Aggregates structured employee data from all chunks
8. Displays in UI and exports as CSV/JSON

## Output Format

```json
[
  {
    "name": "Jane Doe",
    "title": "Chief Marketing Officer",
    "location": "New York",
    "Source URL": "https://example.com/team"
  }
]
```

## Prompt Used by GPT

```
You are an information extraction assistant. Given text from a web page, extract all employee or leadership entries.

Return a list of JSON objects with:
- name
- title
- location (optional)

If no valid entries, return an empty list []
```

## Local Development

### 1. Clone this repo

```bash
git clone https://github.com/your-org/llm-employee-extractor.git
cd llm-employee-extractor
```

### 2. Create a .env file

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4. Run the app

```bash
streamlit run ui_app.py
```

## Docker Deployment

```bash
docker build -t llm-employee-extractor .
docker run -p 8501:8501 --env-file .env llm-employee-extractor
```

## Fly.io Deployment

```bash
flyctl launch
flyctl secrets set OPENAI_API_KEY=sk-xxxx
flyctl deploy
```

## Streamlit Cloud Limitations

Streamlit Cloud does not support Playwright or headless Chromium.

Recommended: Use Fly.io, Render, or a local Docker container for full JavaScript-rendered page support.

## Configuration

- depth: Max recursion depth when crawling
- max_pages: Maximum number of pages to visit
- output_format: Choose CSV or JSON
- chunk_size: Size of text chunk passed to GPT (default 3000 chars)

