from flask import (
  Blueprint, jsonify
)
from flask_jwt_extended import jwt_required
import random
import requests
from ....req_headers.req_headers import req_header

bp = Blueprint('movie', __name__, url_prefix='/api/v1/movie')

@bp.route('/trending')
@jwt_required()
def trending():
  url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch trending movies.', 'error': response.text}), response.status_code

  random_content_list = response.json()["results"]
  random_content = random_content_list[random.randrange(0, len(random_content_list))]

  return jsonify({'message': 'A trending content fetched successfully.', 'response': random_content}), 200

@bp.route('/<movie_id>/trailers')
@jwt_required()
def trending_trailers(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "/videos?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch content trailers.', 'error': response.text}), response.status_code

  trailers = response.json()["results"]

  return jsonify({'message': 'Trailers fetched successfully.', 'reponse': trailers}), 200

@bp.route('/<movie_id>/details')
@jwt_required()
def movie_details(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch details.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Details fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<movie_id>/similar')
@jwt_required()
def similar_movies(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "/similar?language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch similar movies.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Similar movies fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<category>')
@jwt_required()
def movie_category(category):
  url = "https://api.themoviedb.org/3/movie/" + category + "?language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch movies in category.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Movies from category fetched successfully.', 'reponse': response.json()}), 200
