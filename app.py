"""
ACTIVATE VENV
MINGW64: source venv/Scripts/activate
Windows command: venv/Scripts/activate

RUN FLASK APP
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

PUSH TO GITHUB
git add .
git commit -m ""
git push -u origin master

PUSH TO HEROKU
git push heroku master

Add Libraries and Create a requirements.txt File
pip freeze > requirements.txt
"""
from beem import Hive
from beem.nodelist import NodeList
from beem.account import Account

from flask import Flask, render_template, redirect
from forms import UserNameForm
from markupsafe import escape
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

# logging.warning("APP STARTED")


@app.errorhandler(404)
def not_found(e):
    form = UserNameForm()
    return render_template('index.html', form=form)


@app.route('/', methods=('GET', 'POST'))
def index():
    form = UserNameForm()
    if form.validate_on_submit():
        username = form.username.data.lower()

        # return redirect(url_for('friends'))
        return redirect('/friends/' + username)

    return render_template('index.html', form=form)


@app.route('/friends')
@app.route('/friends/<username>')
@app.route('/friends/<username>/')
def friends(username=None):
    data = {}
    if username:
        username = escape(username).lower()
        data['followers'] = get_friends_data(username, 'followers')
        data['following'] = get_friends_data(username, 'following')

    return render_template('friends.html', data=data)


def get_friends_data(username, follow_type):
    # Setup node list
    nodelist = NodeList()
    nodelist.update_nodes()
    nodes = nodelist.get_hive_nodes()
    hive = Hive(node=nodes)
    hive.set_default_nodes(nodes)
    # logging.warning(hive.config.items())

    # Create account object
    try:
        account = Account(username)
        logging.warning(account)
    except Exception as e:
        logging.warning(e)
        return {}

    followers = account.get_followers()
    following = account.get_following()

    if follow_type == 'followers':
        return make_dict(followers, following)
    else:
        return make_dict(following, followers)


def make_dict(data_list, find_list):
    my_dict = {}

    for data in data_list:
        if data in find_list:
            my_dict[data] = 1
        else:
            my_dict[data] = 0
    return my_dict
