import os
import logging
import json
import certifi
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Setup
load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()
openai_api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=openai_api_key
)

# Prompt template
extract_prompt = PromptTemplate.from_template("""
You are an information extraction assistant. Given text from a web page, extract all employee or leadership entries.

Return a list of JSON objects with the following fields:
- name: full name
- title: role or position
- location: if available (optional)

### Example Format:
[
  {{ "name": "John Smith", "title": "VP of Sales", "location": "New York" }},
  {{ "name": "Jane Doe", "title": "CEO", "location": null }}
]

If no names or titles are found, return an empty list [].

Text:
{text}
""")

def extract_employees_from_llm_chunked(text: str, chunk_size: int = 3000, overlap: int = 500) -> list:
    """
    Processes the body text in overlapping chunks and merges employee results.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    all_employees = []
    for i, chunk in enumerate(chunks):
        try:
            formatted_prompt = extract_prompt.format(text=chunk)
            logger.info(f"Calling LLM on chunk {i+1}/{len(chunks)}")
            response = llm.invoke(formatted_prompt)
            result = response.content.strip()

            logger.info(f"Chunk {i+1} raw result: {result[:150]}...")
            employees = json.loads(result)

            if isinstance(employees, list):
                all_employees.extend(employees)
        except Exception as e:
            logger.exception(f"Chunk {i+1} failed to process")

    return all_employees
