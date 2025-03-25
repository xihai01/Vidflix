from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import re
import random
import requests
from .schema import User
from .req_headers.req_headers import movie_req_header

bp = Blueprint('movie', __name__, url_prefix='/movie')

@bp.route('/trending')
def trending():
  url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

  response = requests.get(url, headers=movie_req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch trending movies.', 'error': response.text}), response.status_code

  random_content_list = response.json()["results"]
  random_content = random_content_list[random.randrange(0, len(random_content_list))]

  return jsonify({'message': 'A trending content fetched successfully.', 'response': random_content}), 200

@bp.route('/<movie_id>/trailers')
def trending_trailers(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "/videos?language=en-US"

  response = requests.get(url, headers=movie_req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch content trailers.', 'error': response.text}), response.status_code

  trailers = response.json()["results"]

  return jsonify({'message': 'Trailers fetched successfully.', 'reponse': trailers}), 200

@bp.route('/<movie_id>/details')
def movie_details(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "?language=en-US"

  response = requests.get(url, headers=movie_req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch details.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Details fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<movie_id>/similar')
def similar_movies(movie_id):
  url = "https://api.themoviedb.org/3/movie/" + movie_id + "/similar?language=en-US&page=1"

  response = requests.get(url, headers=movie_req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch similar movies.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Similar movies fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<category>')
def movie_category(category):
  url = "https://api.themoviedb.org/3/movie/" + category + "?language=en-US&page=1"

  response = requests.get(url, headers=movie_req_header())

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch movies in category.', 'error': response.text}), response.status_code

  return jsonify({'message': 'Movies from category fetched successfully.', 'reponse': response.json()}), 200
