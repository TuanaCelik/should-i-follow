import os
from dotenv import load_dotenv

load_dotenv()
TWITTER_BEARER = os.getenv('TWITTER_BEARER_TOKEN')