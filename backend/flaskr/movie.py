from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import re
import random
import requests
from .schema import User

bp = Blueprint('movie', __name__, url_prefix='/movie')

@bp.route('/trending')
def trending():
  url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYWRhNmIxODg5ODEyMDc3ODBkMGY1NGZiZDQ3YjMwOSIsIm5iZiI6MTc0Mjc1NjA5OS4wMjQ5OTk5LCJzdWIiOiI2N2UwNTkwMzk3OGJkYThhZTI0ZGI1OGQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.uasSQi3R9_WqUByZi7oeEJMv9Uc4nUGJouWCBouZC6A"
  }

  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    return jsonify({'message': 'Failed to fetch trending movies.', 'error': response.text}), response.status_code

  random_content_list = response.json()["results"]
  random_content = random_content_list[random.randrange(0, len(random_content_list))]

  return jsonify({'message': 'A trending content fetched successfully.', 'response': random_content}), 200

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
      return jsonify({'message': 'All fields are required.'}), 400

    user = User.objects(username=username).first()
    if not user:
      return jsonify({'message': 'Invalid credentials.'}), 400

    if not check_password_hash(user.password, password):
      return jsonify({'message': 'Invalid credentials.'}), 400

    access_token = create_access_token(identity=user.id)
    response_obj = {
      "username": user.username,
      "email": user.email,
      "image": user.image,
      "access_token": access_token
    }

    return jsonify({'message': 'User logged in successfully.', "user": response_obj}), 200

@bp.route('/logout')
@jwt_required()
def logout():
  user = get_jwt_identity()
  if User.objects(id=user).first():
    return jsonify({'message': 'User logged out successfully.', 'current_user': user}), 200

  return jsonify({'message': 'Error logging out. User not found.'}), 404
