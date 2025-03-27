from flask import (
  Blueprint, jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
import random
import requests
from ..req_headers.req_headers import req_header
from ..database.schema import User

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/person/<query>')
@jwt_required()
def search_by_person(query):
  url = "https://api.themoviedb.org/3/search/person?query=" + query + "&include_adult=false&language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200 or len(response.json()['results']) == 0 :
    return jsonify({'message': 'Failed to fetch by search query.', 'error': response.text}), response.status_code

  # update user model with search history
  user_id = get_jwt_identity();
  user = User.objects(_id=user_id).first()

  if user is None:
    return jsonify({'message': 'Resource not found'}), 404

  response_data = response.json()["results"]
  search_history = {
    'id_n': response_data[0]['id'],
    'image': response_data[0]['profile_path'],
    'title': response_data[0]['name'],
    'search_type': 'person',
    'created_at': date.today().strftime("%A %d. %B %Y")
  }

  User.objects(_id=user_id).update_one(push__search_history=search_history)
  user.reload()

  return jsonify({'message': 'Search history saved successfully.', 'response': response_data}), 200

@bp.route('/movie/<query>')
@jwt_required()
def search_by_movie(query):
  url = "https://api.themoviedb.org/3/search/movie?query=" + query + "&include_adult=false&language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200 or len(response.json()['results']) == 0 :
    return jsonify({'message': 'Failed to fetch by search query.', 'error': response.text}), response.status_code

  # update user model with search history
  user_id = get_jwt_identity();
  user = User.objects(_id=user_id).first()

  if user is None:
    return jsonify({'message': 'Resource not found'}), 404

  response_data = response.json()["results"]
  search_history = {
    'id_n': response_data[0]['id'],
    'image': response_data[0]['poster_path'],
    'title': response_data[0]['title'],
    'search_type': 'movie',
    'created_at': date.today().strftime("%A %d. %B %Y")
  }

  User.objects(_id=user_id).update_one(push__search_history=search_history)
  user.reload()

  return jsonify({'message': 'Search history saved successfully.', 'response': response_data}), 200

@bp.route('/tv/<query>')
@jwt_required()
def search_by_tv(query):
  url = "https://api.themoviedb.org/3/search/tv?query=" + query + "&include_adult=false&language=en-US&page=1"

  response = requests.get(url, headers=req_header())

  if response.status_code != 200 or len(response.json()['results']) == 0 :
    return jsonify({'message': 'Failed to fetch by search query.', 'error': response.text}), response.status_code

  # update user model with search history
  user_id = get_jwt_identity();
  user = User.objects(_id=user_id).first()

  if user is None:
    return jsonify({'message': 'Resource not found'}), 404

  response_data = response.json()["results"]
  search_history = {
    'id_n': response_data[0]['id'],
    'image': response_data[0]['poster_path'],
    'title': response_data[0]['name'],
    'search_type': 'tv',
    'created_at': date.today().strftime("%A %d. %B %Y")
  }

  User.objects(_id=user_id).update_one(push__search_history=search_history)
  user.reload()

  return jsonify({'message': 'Search history saved successfully.', 'response': response_data}), 200
