from dotenv import load_dotenv
import os
from groq import Groq
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import nltk

load_dotenv(".env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

nltk.download("punkt_tab")
def clean_text(text):
    sentences = sent_tokenize(text)
    cleaned_text = ' '.join(sentences[:50])
    return cleaned_text

def summarize_text(input_text):
    try:
        res = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and smart assistant.that summarizes text in meaningful and concise terms and no more than 320 words. Return only the summary.",
                },
                {
                    "role": "user",
                    "content": f"Summarize this text:\n\n{input_text}",
                },
            ],
            temperature=0.5,
            max_tokens=320,
            model="llama-3.1-8b-instant",
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return None     

    summary = res.choices[0].message.content
    return {"data": summary}

def scrape_url(url:str):
    try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to get content from {url}")
                return None

            soup = BeautifulSoup(response.content, 'html.parser')
            print("Scrapping finished. Cleaning...")

            paragraphs = soup.find_all('p')
            page_text = ' '.join([p.text for p in paragraphs])
            cleaned_text = clean_text(page_text)

            if not cleaned_text or len(cleaned_text.strip()) < 50:
                print("Not enough content to summarize.")
                return None
            print("Cleaning finished. Summarizing to start soon...")
            return cleaned_text
    except Exception as e:
        print(f"An error occurred while scraping : {e}")
        return None
