from flask import Blueprint, jsonify, request
from app.tmdb_client import (
    get_popular_movies, 
    get_top_rated_movies, 
    get_upcoming_movies, 
    get_movie_details,
    search_movies
)
from app import cache

movies_bp = Blueprint('movies_v1', __name__)

@movies_bp.route('/popular', methods=['GET'])
@cache.cached(timeout=900)
def popular_movies():
    movies, error = get_popular_movies()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(movies)

@movies_bp.route('/top-rated', methods=['GET'])
@cache.cached(timeout=900)
def top_rated_movies():
    movies, error = get_top_rated_movies()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(movies)

@movies_bp.route('/upcoming', methods=['GET'])
@cache.cached(timeout=900)
def upcoming_movies():
    movies, error = get_upcoming_movies()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(movies)

@movies_bp.route('/<int:movie_id>', methods=['GET'])
@cache.cached(timeout=3600)
def movie_details(movie_id):
    details, error = get_movie_details(movie_id)
    if error:
        if "not found" in error.lower():
            return jsonify({"error": error}), 404
        return jsonify({"error": error}), 500
    return jsonify(details)

@movies_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('title')
    page = request.args.get('page', 1, type=int)

    if not query:
        return jsonify({"error": "A 'title' query parameter is required."}), 400

    results, error = search_movies(query, page)
    if error:
        return jsonify({"error": error}), 500
        
    return jsonify(results)