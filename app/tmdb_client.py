import requests
import colorgram
import io
from flask import current_app
from thefuzz import process as fuzzy_process

def _make_tmdb_request(endpoint, params=None):
    base_url = "https://api.themoviedb.org/3"
    api_key = current_app.config.get('TMDB_API_KEY')
    
    if not api_key:
        return None, "TMDB_API_KEY not configured"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try: 
        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    
    except requests.exceptions.RequestException as e:
        return None, str(e)
    
def _process_movie_list(movie_data):
    if not movie_data or 'results' not in movie_data:
        return []
    
    processed_movies = []
    for movie in movie_data['results']:
        if movie.get('poster_path'):
            processed_movies.append({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'overview': movie.get('overview'),
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                'rating': movie.get('vote_average')
            })
            
    return processed_movies

def get_popular_movies():
    data, error = _make_tmdb_request("movie/popular")
    if error:
        return None, error
    return _process_movie_list(data), None

def get_top_rated_movies():
    data, error = _make_tmdb_request("movie/top_rated")
    if error:
        return None, error
    # FIX: Corrected a small typo from a previous version (.data -> data)
    return _process_movie_list(data), None

def get_upcoming_movies():
    data, error = _make_tmdb_request("movie/upcoming")
    if error:
        return None, error
    return _process_movie_list(data), None

def _get_palette_from_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        img = io.BytesIO(response.content)
        colors = colorgram.extract(img, 6)
        
        return [f'#{c.rgb.r:02x}{c.rgb.g:02x}{c.rgb.b:02x}' for c in colors]
    except Exception as e:
        print(f"Color extraction failed: {e}")
        return []
    
def get_movie_details(movie_id):
    details_data, error = _make_tmdb_request(f"movie/{movie_id}")
    if error:
        return None, error
    
    credits_data, error = _make_tmdb_request(f"movie/{movie_id}/credits")
    if error:
        credits_data = {}
        
    videos_data, error = _make_tmdb_request(f"movie/{movie_id}/videos", params={"language": "en-US"})
    if error:
        videos_data = {}
        
    if not details_data:
        return None, "Movie not found"
    
    cast = [{"name": member['name'], "character": member['character'], "profile_path": f"https://image.tmdb.org/t/p/w185{member['profile_path']}" if member.get('profile_path') else None} for member in credits_data.get('cast', [])[:10]]
    
    trailer = next((video for video in videos_data.get('results', []) if video['type'] == 'Trailer' and video['site'] == 'YouTube'), None)
    
    poster_url = f"https://image.tmdb.org/t/p/w500{details_data.get('poster_path')}" if details_data.get('poster_path') else None
    
    palette = _get_palette_from_image(poster_url) if poster_url else []
    
    combined_details = {
        "id": details_data.get('id'),
        "title": details_data.get('title'),
        "overview": details_data.get('overview'),
        "poster_url": poster_url,
        "backdrop_url": f"https://image.tmdb.org/t/p/w1280{details_data.get('backdrop_path')}" if details_data.get('backdrop_path') else None,
        "rating": details_data.get('vote_average'),
        "release_date": details_data.get('release_date'),
        "runtime": details_data.get('runtime'),
        "genres": [genre['name'] for genre in details_data.get('genres', [])],
        "cast": cast,
        "trailer": { "key": trailer['key'], "url": f"https://www.youtube.com/watch?v={trailer['key']}" } if trailer else None,
        "color_palette": palette
    }
    
    return combined_details, None

def search_movies(query, page=1):
    """
    Searches for movies using the TMDB API.
    The fuzzy matching has been removed to ensure reliability.
    """
    search_data, error = _make_tmdb_request("search/movie", params={"query": query, "page": page})
    if error:
        return None, error

    if not search_data or 'results' not in search_data or not search_data['results']:
        return {"results": [], "total_pages": 0, "total_results": 0}, None

    processed_results = _process_movie_list(search_data)
    
    return {
        "results": processed_results,
        "page": search_data.get('page'),
        "total_pages": search_data.get('total_pages'),
        "total_results": search_data.get('total_results')
    }, None