from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv(".env")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
