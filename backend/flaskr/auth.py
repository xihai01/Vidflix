import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import re
import random
from .schema import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    email_regex = r'^\S+@\S+$'
    images = ['/avatar1.png', '/avatar2.png', '/avatar3.png']
    profile_pic = images[random.randint(0, 2)]

    if not username:
      return jsonify({'message': 'The field username is required.'}), 400
    elif not password:
      return jsonify({'message': 'The field password is required.'}), 400
    elif not email:
      return jsonify({'message': 'The field email is required.'}), 400

    if not re.match(email_regex, email):
      return jsonify({'message': 'The field email must be a valid email address.'}), 400

    if len(password) < 8:
      return jsonify({'message': 'The field password must be at least 8 characters long.'}), 400

    if User.objects(username=username).first():
      return jsonify({'message': 'This username is already registered.'}), 400

    if User.objects(email=email).first():
      return jsonify({'message': 'This email is already registered.'}), 400

    new_user = User(
      _id=str(User.objects.count() + 1),
      username=username,
      email=email,
      password=generate_password_hash(password, method='pbkdf2:sha256'),
      image=profile_pic
    )

    access_token = create_access_token(identity=new_user.id)
    new_user.save()

    response_obj = {
      "username": new_user.username,
      "email": new_user.email,
      "image": new_user.image,
      "access_token": access_token
    }

    return jsonify({'message': 'User created successfully.', "user": response_obj}), 201

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
