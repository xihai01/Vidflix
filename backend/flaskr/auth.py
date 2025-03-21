import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
import re
import random
from .schema import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

'''
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
'''

'''
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)

  return wrapped_view'
'''

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    email_regex = r'^\S+@\S+$'
    image = ['/avatar1.png', '/avatar2.png', '/avatar3.png']
    profile_pics = image[random.randint(0, 2)]
    #db = get_db()
    #error = None

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
      username=username,
      email=email,
      password=generate_password_hash(password, method='pbkdf2:sha256'),
      image=profile_pics
    )

    new_user.save()

    #if error is None:
      #try:
        #db.execute(
         # 'INSERT INTO user (username, password) VALUES (?, ?)',
          #(username, generate_password_hash(password))
        #)
        #db.commit()
      #except db.IntegrityError:
        #error = f"User {username} is already registered."
      #else:
        #return redirect(url_for('auth.login'))

      #flash(error)

    response_obj = {
      "username": new_user.username,
      "email": new_user.email,
      "image": new_user.image
    }

    return jsonify({'message': 'User created successfully.', "user": response_obj}), 201

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    #username = request.form['username']
    #password = request.form['password']
    #db = get_db()
    #error = None
    #user = db.execute(
     # 'SELECT * FROM user WHERE username = ?', (username,)
    #).fetchone()
    '''
    if user is None:
      error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)'
    '''
    return jsonify({'message': 'login route'})

@bp.route('/logout')
def logout():
  #session.clear()
  #return redirect(url_for('index'))
  return jsonify({'message': 'logout route'})
