#!/usr/bin/env python
import io
import locale
import pickle
from sqlite3 import DatabaseError

import bottle
from bottle import template, static_file, redirect, request, get, post, route
from beaker.middleware import SessionMiddleware
from sqlite3 import DatabaseError
from random import choice

from db_utils.users import UserDatabase, User

locale.setlocale(locale.LC_ALL, '')

user_db = UserDatabase('db/user_database.db')

session_opts = {
    'session.cookie_expires': 3000,
    'session.encrypt_key': 'TEST KEY PLEASE IGNORE',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'memory',
    'session.validate_key': True,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


###############################################################################
# Session Functions ###########################################################
###############################################################################

def get_session():
    return bottle.request.environ.get('beaker.session')


def login_session(username):
    s = get_session()
    user_table = user_db.table(User)
    user_row = user_table.get(username)
    s['username'] = user_row['Username']
    s['permissions'] = user_row['Permissions']
    s['has_picture'] = user_row['Picture'] is not None


###############################################################################
# Routes ######################################################################
###############################################################################

@get('/login', name='login')
@post('/login')
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if user_db.validate_login(username, password):
            login_session(username)
            redirect('/')
        else:
            return template('invalid_login', sess=get_session())
    return template('login', sess=get_session())


@get('/update_profile/self')
def update_profile():
    return template('update_profile', sess=get_session())


@post('/change_password')
def change_password():
    s = get_session()
    username = s['username']
    current_password = request.forms.get('current_password')
    new_password = request.forms.get('new_password')
    if user_db.validate_login(username, current_password):
        user_db.update_password(username, new_password)
        return template('update_profile', success=True, sess=s)
    return template('update_profile', success=False, sess=s)


@post('/change_picture')
def change_picture():
    s = get_session()
    new_picture = request.files.get('picture')  # type: bottle.FileUpload
    with new_picture.file as pic:
        img_set = {'length': new_picture.content_length,
                   'type': new_picture.content_type,
                   'data': pic.read()}
    img_data = pickle.dumps(img_set)
    try:
        user_db.update_picture(s['username'], img_data)
    except DatabaseError:
        return template('update_profile', success=False, sess=s)
    s['has_picture'] = True
    return template('update_profile', success=True, sess=s)


@route('/logout', name='logout')
def logout():
    s = get_session()
    if 'username' in s:
        del s['username']
        del s['permissions']
        del s['has_picture']
    redirect('/')


@route('/user/<username>', name='user_page')
def user(username):
    return {}  # TODO: Create user page.


@route('/admin', name='admin')
def admin():
    s = get_session()
    if not user_db.authorize(s['username']):
        redirect('/denied')
    return {}  # TODO: Create admin page.


@get('/create_user')
@post('/create_user')
def create_user():
    if request.method == 'POST':
        username = request.forms['username']
        role = request.forms['role']
        ranges = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
        temp_password = "".join([chr(choice(ranges)) for i in range(12)])
        try:
            user_db.add_user(username, temp_password, role)
            return template('create_user_success', sess=get_session(), user=username, pw=temp_password)
        except DatabaseError as e:
            return {'ok': False, 'msg': e}
    else:
        return template('create_user', sess=get_session())


@route('/', name='index')
def index():
    s = bottle.request.environ.get('beaker.session')
    if 'username' not in s:
        redirect('/login')
    else:
        return template('index', sess=get_session())



@get('/question', name='ask_question')
def ask_question():
    return template('question', sess=get_session())

@get('/upload', name='upload_file')
def upload_file():
    return template('upload', sess=get_session())

@get('/viewdownload', name='view_download')
def view_download():
    return template('viewdownload', sess=get_session())



@route('/denied', name='denied')
def denied():
    return template('denied', sess=get_session())


@route('/static/<file:path>')
def send_static(file):
    return static_file(file, root='static/')


@route('/profile/<username>/image')
def send_profile_image(username):
    user_table = user_db.table(User)
    user_row = user_table.get(username)
    img_data = user_row['Picture']
    img_set = pickle.loads(img_data)  # type: dict
    bottle.response.set_header('Content-Type', img_set.get('type'))
    bottle.response.set_header('Content-Length', img_set.get('length'))
    return io.BytesIO(img_set.get('data'))


if __name__ == "__main__":
    bottle.run(app=app, host='localhost', port=8080, reloader=True, debug=True)
