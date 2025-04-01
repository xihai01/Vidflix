from flask import (
  Blueprint, request, jsonify, abort
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import re
import random
from ....database.schema import User

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

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
      abort(400, description="The field username is required.")
    elif not password:
      abort(400, description="The field password is required.")
    elif not email:
      abort(400, description="The field email is required.")

    if not re.match(email_regex, email):
      abort(400, description="The field email must be a valid email address.")

    if len(password) < 8:
      abort(400, description="The field password must be at least 8 characters long.")

    if User.objects(username=username).first():
      abort(400, description="This username is already registered.")

    if User.objects(email=email).first():
      abort(400, description="This email is already registered.")

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
      abort(400, description="All fields are required.")

    user = User.objects(username=username).first()
    if not user:
      abort(400, description="Invalid credentials.")

    if not check_password_hash(user.password, password):
      abort(400, description="Invalid credentials.")

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

  abort(404, description="Error logging out. User not found.")
