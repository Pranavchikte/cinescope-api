import pytest
from app import create_app
from config import Config
from dotenv import load_dotenv 
import os 

load_dotenv()

class TestConfig(Config):
    TESTING = True
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

@pytest.fixture
def client():
    app = create_app(TestConfig)
    
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_get_popular_movies(client):
    
    response = client.get('/api/v1/movies/popular')
    
    assert response.status_code == 200
    
    assert response.content_type == 'application/json'
    
    response_data = response.get_json()
    assert isinstance(response_data, list)
    
    assert len(response_data) > 0

def test_get_movie_details_404(client):

    non_existent_id = 99999999
    response = client.get(f'/api/v1/movies/{non_existent_id}')
    
    assert response.status_code == 404
    
    response_data = response.get_json()
    assert 'error' in response_data
    assert 'not found' in response_data['error'].lower()