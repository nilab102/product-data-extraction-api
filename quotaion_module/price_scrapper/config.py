import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and URLs
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # e.g., "364d026767c7e9e9a3cdacbef32929efe73abe88"
LLM_API_KEY = os.getenv("LLM_API_KEY")          # e.g., "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"
ZENROWS_API_KEY=os.getenv("ZENROWS_API_KEY")   
SERPER_URL = "https://google.serper.dev/search"
SERPER_LOCATION = "Saudi Arabia"
SERPER_GL = "sa"

# Allowed domains for filtering search results
ALLOWED_DOMAINS = [
    "amazon",
    "ebay",
    "bestbuy",
    "shareefcorner",
    "noon",
    "jarir",
    "electroon"
]

# Chunking settings
CHUNK_SIZE = 10000
CHUNK_OVERLAP = 500

# Selenium Chrome options (if you wish to customize further)
CHROME_OPTIONS = [
    "--headless",  # Run in headless mode
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
