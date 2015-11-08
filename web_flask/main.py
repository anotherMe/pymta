#!/usr/bin/python2


import flask
from flask import request
import flask.ext.login as fLogin
import json
from datetime import date as dt

import models

from database import DB
DATABASE = '/home/marco/lab/pymta/yahoo.db3' ## FIXME: move in a configuration file

app = flask.Flask(__name__)
app.secret_key = '\x9b\x8a\x98\xe9r \xcc\n\xe3\x16\xe1\xe7\xad\x8c\x8ee|uY\x9d b\xf4W'
login_manager = fLogin.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	
	user = models.User('pippo', 'fasdfasdfasdfa')
    return user.get(user_id)
    

def get_db():
	"""Return current database instance; creating it, if not exists."""
	db = getattr(flask.g, '_database', None)
	if db is None:
		db = flask.g._database = DB(DATABASE)
	return db

# Add a custom static data ( apart from the default "static" folder )
@app.route('/bower_components/<path:filename>')
def custom_static(filename):
    #~ return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename)
    return flask.send_from_directory('bower_components', filename)


@app.teardown_appcontext
def close_connection(exception):
	
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.dispose()
        

@app.route('/get_eod/<symbol>/')
@app.route('/get_eod/<symbol>/<mindate>/')
@app.route('/get_eod/<symbol>/<mindate>/<maxdate>/')
def get_eod(symbol, mindate=None, maxdate=None):

	db = get_db()
	rows = db.get_eod(symbol, mindate, maxdate)
	return json.dumps(rows)


@app.route('/symbol/search/<search_string>/')
def symbol_search(search_string):

	db = get_db()
	rows = db.search_symbol(search_string)
	return json.dumps(rows)


@app.route('/')
def default():
	return flask.render_template('index.html')

@app.route('/plot/')
def plot():
	return flask.render_template('plot.html')


@app.route('/test/')
def test():
	return flask.render_template('login.html')
	
	
def checkUser(email, password):
	if name == 'armando@gmail.com':
		return True
	else:
		return False
		
	
@app.route('/login/', methods=['GET', 'POST'])
def login():
	
	errorMsg = None
	if flask.request.method == 'POST':
		if checkUser(request.form['inputEmail'],request.form['inputPassword']):

			#~ next = flask.request.args.get('next')
			#~ if not next_is_valid(next):
				#~ return flask.abort(400)
			#~ return flask.redirect(next or flask.url_for('index'))
			return "You logged in !"
			
		else:
			errorMsg = 'Invalid username/password'
	
	return flask.render_template('login.html', loginErrorMsg=errorMsg)
    
@app.route("/testlogin/")
@fLogin.login_required
def testlogin():
    return "Hello, logged in user"

if __name__ == '__main__':
	
	app.run(debug=True)

