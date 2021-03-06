#!/usr/bin/env python
import io
import locale
import pickle
import os
from sqlite3 import DatabaseError
import warnings
import bottle
from bottle import template, static_file, redirect, request, get, post, route
from beaker.middleware import SessionMiddleware
from sqlite3 import DatabaseError
from random import choice

from db_utils.users import UserDatabase, User
from helpers import *
from file_manip import load_questions, load_model, save_response

locale.setlocale(locale.LC_ALL, '')
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")  # ignore this (just to supress warning)
user_db = UserDatabase('db/user_database.db')

session_opts = {
    'session.cookie_expires': 3600 * 24,  # 1 day
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'memory',
    'session.validate_key': True,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)


# Globals
QUESTIONS = load_questions('data/questions.txt')


# MODEL = train_model()
# # it's easier to load the model from a save
# than to  train every time its opened
MODEL = load_model()


###############################################################################
# Session Functions ###########################################################
###############################################################################
def user_is_mobile():
    agent = request.headers.get('User-Agent')
    phones = ["iphone", "android", "blackberry", "windows phone"]
    if any(phone in agent.lower() for phone in phones):
        return True
    return False


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


@get('/create_user')
@post('/create_user')
def create_user():
    if request.method == 'POST':
        username = request.forms['username']
        role = request.forms['role']
        ranges = list(range(48, 58)) + list(range(65, 91)) + \
            list(range(97, 123))
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
    return template('index', sess=get_session())


@get('/start_interview', name='start_interview')
def start_interview():
    session = get_session()
    session['current_question'] = 0
    session['answers'] = []
    redirect('/question')


@post('/question')
@get('/question', name='ask_question')
def ask_question():
    session = get_session()
    if 'current_question' not in session:
        redirect('/')
    if request.method == 'POST':

        session['answers'].append(request.forms.get(
            'answer').replace('\r\n', ' ').strip())
        session['current_question'] += 1
        if session['current_question'] >= len(QUESTIONS):
            session['survey_complete'] = True
            redirect('/show_results')
        return template('question', sess=get_session(), index=session['current_question'] + 1, question=QUESTIONS[session['current_question']], num_questions=len(QUESTIONS))
    else:
        return template('question', sess=get_session(), index=session['current_question'] + 1, question=QUESTIONS[session['current_question']], num_questions=len(QUESTIONS))


@route('/show_results', name='show_results')
def show_results():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')

    redirect('/choose_view_format')


@route('/choose_view_format', name='choose_view_format')
def choose_view_format():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')
    if not "".join(session["answers"][1:]): # if no questions answered
        return template('index', sess=get_session())
    save_response(session["answers"][0], "\t".join(session["answers"][1:]))
    if user_is_mobile():
        redirect('/big5')
    else:
        return template('choose_view_format', sess=get_session())


@route('/download/<filename:path>')
def download(filename):
    s = get_session()
    if not 'username' in s:
        redirect('/denied')
    return static_file(filename, root=os.getcwd() + '/data', download=filename)


@route('/upload_model', method='POST')
def do_upload():
    s = get_session()
    if not 'username' in s:
        redirect('/denied')
    upload = request.files.get('filename')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.npz':
        return 'File extension not allowed.'  # TODO: make a nicer page for this
    upload.filename = "model.npz"
    save_path = os.getcwd() + "/data/weight_matrix"
    # appends upload.filename automatically
    upload.save(save_path, overwrite=True)
    MODEL = load_model()
    # TODO: make a "successful upload" page
    return template('index', sess=get_session())

@route('/upload_train_data', method='POST')
def do_upload_train():
    s = get_session()
    if not 'username' in s:
        redirect('/denied')
    upload = request.files.get('filename')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.csv':
        return 'File extension not allowed.'  # TODO: make a nicer page for this
    upload.filename = "results.csv"
    save_path = os.getcwd()
    # appends upload.filename automatically
    upload.save(save_path, overwrite=True)
    process_new_csv("results.csv")
    MODEL = train_model()
    # TODO: make a "successful train"
    return template('index', sess=get_session())

@route('/thank_you', name='thank_you')
def thank_you():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')
    del session['survey_complete']
    del session['current_question']
    del session['answers']
    return template('thank_you', sess=get_session())


@route('/raw', name='raw')
def raw():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')
    feature_scores = extract_features(" ".join(session['answers'][1:]))[
        1].reshape(1, -1)
    results = MODEL.predict(feature_scores)[0]
    snap_boundaries(results)
    generate_report(results)
    # return template('choose_view_format', sess=get_session())
    return static_file("visualize.html", os.getcwd())

@route('/big5', name='big5')
def big5():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')
    feature_scores = extract_features(" ".join(session['answers'][1:]))[
        1].reshape(1, -1)
    results = MODEL.predict(feature_scores)[0]
    snap_boundaries(results)
    big5_radar(results)
    # return template('choose_view_format', sess=get_session())
    return static_file("visualize.html", os.getcwd())


@route('/percentile', name='percentile')
def percentile():
    session = get_session()
    if not 'survey_complete' in session:
        redirect('/')
    feature_scores = extract_features(" ".join(session['answers'][1:]))[
        1].reshape(1, -1)
    results = MODEL.predict(feature_scores)[0]
    snap_boundaries(results)
    generate_report_comparison(results)
    # return template('choose_view_format', sess=get_session())
    return static_file("visualize.html", os.getcwd())


@get('/upload_model', name='upload_model')
def upload_model():
    return template('upload_model', sess=get_session())

@get('/upload_train_page', name='upload_train_page')
def upload_train_page():
    return template('upload_train_page', sess=get_session())

@get('/upload', name='upload')
def upload():
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
