
import flask as f
app = f.Flask(__name__)

import json
from datetime import date as dt
import pdb


from database import DB
DATABASE = '/home/marco/lab/python/yahoo.db3'



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
        

@app.route('/get_data/<symbol>/')
@app.route('/get_data/<symbol>/<mindate>/')
@app.route('/get_data/<symbol>/<mindate>/<maxdate>/')
def get_data(symbol, mindate=None, maxdate=None):

	db = get_db()
	rows = db.select_rows(symbol, ["date", "open", "high", "low", "close", "volume"], mindate, maxdate)
	return json.dumps(rows)


@app.route('/plot/<type>/<symbol>/')
@app.route('/plot/<type>/<symbol>/<mindate>/')
@app.route('/plot/<type>/<symbol>/<mindate>/<maxdate>/')
def plot(type, symbol, mindate=None, maxdate=None):
	
	if mindate==None:
		mindate = dt(dt.today().year, 1, 1).isoformat()
		
	return f.render_template('candlestick.html', symbol=symbol, mindate=mindate, maxdate=maxdate)
	

@app.route('/')
def default():
	return 'Default route asked.'



if __name__ == '__main__':
	
	app.run(debug=True)
