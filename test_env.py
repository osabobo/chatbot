# test_env.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GROQ_API_KEY from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# Print the API key for debugging
print(f"GROQ_API_KEY: {groq_api_key}")
