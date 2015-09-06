
import sqlite3
import pdb

class DB:
	
	def __init__(self, database_file):
		
		self.conn = sqlite3.connect(database_file)
	
	def get_list_from(self, cursor, rows):
		"""Given a cursor and a list of rows, returns a dictionary."""
		
		my_list = []
		for row in rows:
			obj = {}
			for idx, col in enumerate(cursor.description):
				obj[col[0]] = row[idx]
				
			my_list.append(obj)

		return my_list


	def select_rows(self, symbol, columns, lowerBound=None, higherBound=None):

		sql = "select "
		firstLoop = True
		for column in columns:
			sql += column if firstLoop else ", " + column
			firstLoop = False
		
		#~ sql = "select date, {0} from stocks where symbol = '{1}'".format(column, symbol)
		sql += " from DAT_EoD where symbol = '{1}'".format(column, symbol)
		
		if lowerBound:
			sql = sql + " and date_STR >= strftime('%Y-%m-%d', '{0}')".format(lowerBound)
		
		if higherBound:
			sql = sql + " and date_STR >= strftime('%Y-%m-%d', '{0}')".format(higherBound)
		
		#self.conn.row_factory = sqlite3.Row
		#~ self.conn.row_factory = self.dict_factory 
		
		cur = self.conn.cursor()
		cur.execute (sql)
		rows = cur.fetchall()

		return self.get_list_from(cur, rows)
		

	def dispose(self):
		
		self.conn.close()
