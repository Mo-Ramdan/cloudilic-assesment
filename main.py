from fastapi import FastAPI, HTTPException
from utils import scrape_url , summarize_text
from models import UrlRequest , SummarizeRequest
from fastapi.middleware.cors import CORSMiddleware
import logging
import os 
import nltk

nltk.download("punkt_tab")
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL") , "*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.post("/scrape")
async def scrape_and_summarize(request: UrlRequest):
    """
    Scrape a URL and summarize its content.

    Args:
        request: A URL to scrape and summarize.

    Returns:
        A JSON object with a single key `data` containing the summarized text.

    Raises:
        404: Scraping the URL failed.
        400: Can't scrape or summarize the URL.
    """
    url = request.url
    try:
        logger.info(f"Scraping and summarizing: {url}")
        scrapped_data = scrape_url(url)
        if not scrapped_data:
            logger.warning(f"No scrapped data return for URL: {url}")
            raise HTTPException(
                status_code=404, detail="scraping url failed"
            )
    except Exception as e:
        logger.error(f"Error occurred during scraping: {e}")
        raise HTTPException(status_code=400, detail="Can't scrape or summarize")
    return {"data": scrapped_data}


@app.post("/summarize")
async def summarize(text: SummarizeRequest):
    """
    Summarize a given text.

    Args:
        text: A request object with a single key `data` containing the text to summarize.

    Returns:
        A JSON object with a single key `summary` containing the summarized text.

    Raises:
        400: Can't summarize the text.
    """
    summary = summarize_text(text.data)
    if not summary:
        raise HTTPException(status_code=400, detail="Can't summarize")
    return summary

@app.get("/health")
async def health_check():
    """
    A simple health check endpoint to verify the service is running.

    Returns:
        A JSON object with a single key `status` containing the value `"ok"`.
    """
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Hello in Cloudilic! 🎉"}
