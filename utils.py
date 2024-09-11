import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from llm import client





def clean_text(text):
    """
    Clean a given text by extracting only the first 50 sentences of it.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """

    sentences = sent_tokenize(text)
    cleaned_text = ' '.join(sentences[:50])
    return cleaned_text

def summarize_text(input_text):
    """
    Summarize a given text using Groq's chat completion API.

    Args:
        input_text (str): The text to be summarized.

    Returns:
        dict: A dictionary with a single key-value pair, where the key is "data" and the value is the summarized text.
    """
    try:
        res = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful and smart assistant.that summarizes text in meaningful and concise terms and no more than 320 words. Return only the summary:\n\n{input_text}.",
                }
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
    
    """
    Scrape a given URL, extract all text from the page, clean it up, and return the cleaned text.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        str: The cleaned text. If the request fails or the page does not have enough content to summarize, None is returned.
    """
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
