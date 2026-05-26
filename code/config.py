from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SUPPORT_DIR = BASE_DIR / "support_tickets"
INPUT_CSV = SUPPORT_DIR / "support_tickets.csv"
OUTPUT_CSV = SUPPORT_DIR / "output.csv"
API_SPEC_PATH = DATA_DIR / "api_specs" / "internal_tools.json"
TOP_K_RETRIEVAL = 5
CHUNK_SIZE = 900
CHUNK_OVERLAP = 140
RANDOM_SEED = 7
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
