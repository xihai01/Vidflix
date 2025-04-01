from flask import (
  Blueprint, jsonify, abort
)
from flask_jwt_extended import jwt_required
import random
import requests
from ....req_headers.req_headers import req_header

bp = Blueprint('tv', __name__, url_prefix='/api/v1/tv')

@bp.route('/trending')
@jwt_required()
def trending():
  url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    abort(400, description="Failed to fetch trending tv shows.")

  random_content_list = response.json()["results"]
  random_content = random_content_list[random.randrange(0, len(random_content_list))]

  return jsonify({'message': 'A trending content fetched successfully.', 'response': random_content}), 200

@bp.route('/<tv_id>/trailers')
@jwt_required()
def trending_trailers(tv_id):
  url = "https://api.themoviedb.org/3/tv/" + tv_id + "/videos?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    abort(400, description="Failed to fetch content trailers.")

  trailers = response.json()["results"]

  return jsonify({'message': 'Trailers fetched successfully.', 'reponse': trailers}), 200

@bp.route('/<tv_id>/details')
@jwt_required()
def movie_details(tv_id):
  url = "https://api.themoviedb.org/3/tv/" + tv_id + "?language=en-US"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    abort(400, description="Failed to fetch details.")

  return jsonify({'message': 'Details fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<tv_id>/similar')
@jwt_required()
def similar_movies(tv_id):
  url = "https://api.themoviedb.org/3/tv/" + tv_id + "/similar?language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    abort(400, description="Failed to fetch similar tv shows.")

  return jsonify({'message': 'Similar tv shows fetched successfully.', 'reponse': response.json()}), 200

@bp.route('/<category>')
@jwt_required()
def movie_category(category):
  url = "https://api.themoviedb.org/3/tv/" + category + "?language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200:
    abort(400, description="Failed to fetch tv shows in category.")

  return jsonify({'message': 'Tv shows from category fetched successfully.', 'reponse': response.json()}), 200
