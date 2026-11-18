import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
OPENALEX_MAX_RESULTS = int(os.getenv("OPENALEX_MAX_RESULTS", "8"))
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma")
