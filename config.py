import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "fuck-you-nasty-asshole"
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')