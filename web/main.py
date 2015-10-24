#!/usr/bin/python2


import flask as f
app = f.Flask(__name__)

import json
from datetime import date as dt
import pdb


from database import DB
DATABASE = '/home/marco/lab/pymta/yahoo.db3' ## FIXME: move in a configuration file


# Add a custom static data ( apart from the default "static" folder )
@app.route('/bower_components/<path:filename>')
def custom_static(filename):
    #~ return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename)
    return f.send_from_directory('bower_components', filename)



def get_db():
	"""Return current database instance; creating it, if not exists."""
	db = getattr(f.g, '_database', None)
	if db is None:
		db = f.g._database = DB(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	
    db = getattr(f.g, '_database', None)
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
	return f.render_template('index.html')

@app.route('/plot/')
def plot():
	return f.render_template('plot.html')


if __name__ == '__main__':
	
	app.run(debug=True)

