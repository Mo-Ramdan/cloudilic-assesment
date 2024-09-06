from fastapi import FastAPI, HTTPException
from utils import scrape_then_summarize
from models import UrlRequest
from fastapi.middleware.cors import CORSMiddleware
import logging
import os 

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

@app.post("/scrape-summary")
async def scrape_and_summarize(request: UrlRequest):
    url = request.url
    try:
        logger.info(f"Scraping and summarizing: {url}")
        summary = scrape_then_summarize(url)
        if not summary:
            logger.warning(f"No Summary return for URL: {url}")
            raise HTTPException(
                status_code=404, detail="Summary not found or scraping failed"
            )
    except Exception as e:
        logger.error(f"Error occurred during scraping: {e}")
        raise HTTPException(status_code=400, detail="Can't scrape or summarize")
    return {"data": summary}
