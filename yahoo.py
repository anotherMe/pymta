#!/usr/bin/env python2

import logging
import sqlite3
import urllib
import csv
import datetime
import os

import traceback

URL_CHECK_EXISTENCE = "https://finance.yahoo.com/q?s={0}"
URL_CSV_DOWNLOAD = "http://real-chart.finance.yahoo.com/table.csv"


class Source(object):
	"""Not to be instantiated explicitly. This class is just an interface
	all the data sources should adhere.
	"""

	def __init__(self):
		
		logging.basicConfig(filename='yahoo.log', level=logging.DEBUG, format='%(asctime)s %(message)s') # log to file
		self.logger = logging.getLogger('yahoo')
		#~ logging.getLogger().addHandler(self.logger.StreamHandler()) # log to stderr too
		
	def symbol_get_closings(self):
		raise Exception("Not implemented yet")

	def symbol_get_volumes(self):
		raise Exception("Not implemented yet")

	def symbol_get_ochlv(self):
		raise Exception("Not implemented yet")
		
	def _get_url(self, symbol_name, mindate=None, maxdate=None, historical=True):
		"""Build the URL needed to download data from Yahoo Finance 
		site.
		
		Parameter:
		
			symbol_name: symbol name, according to Yahoo convention (ie: SPM.MI)
			mindate: string representing date in the format '%Y-%m-%d'
			maxdate: string representing date in the format '%Y-%m-%d'
			historical: query Yahoo historical data ( at the moment we know about this only type of data)
		"""
		
		url = URL_CSV_DOWNLOAD + "?s={0}".format(symbol_name)
		
		if mindate != None:
			url += "&a={0}&b={1}&c={2}".format(mindate.month - 1, mindate.day, mindate.year)
			
		if maxdate != None:
			url += "&d={0}&e={1}&f={2}".format(maxdate.month - 1, maxdate.day, maxdate.year)
			
		url += "&g=d" # daily data
		url += "&ignore=.csv"

		return url


class DataError(Exception):
	"""Raised when there's no data available for the requested symbol.
	"""
	
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
		
class OnlineSource(Source):
	
	def __init__(self):
		
		super(OnlineSource, self).__init__()
		#~ Source.__init__(self)

	def _parsedatestring(self, inputdate):
		"""Parameters:
		
			inputdate: a string representing a date in the format '%Y-%m-%d'
			
		Returns an integer, representing the number of seconds since Epoch
		"""
		
		datetime_obj = datetime.datetime.strptime(inputdate, '%Y-%m-%d')
		return int(datetime_obj.strftime('%s'))

	def symbol_get_closings(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'close')
		"""
		
		data = []
		tempfile = self.download2csv(symbol_name, mindate, maxdate)
		f = open(tempfile, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		firstRow = True
		for row in reader:
			
			# skip field names row
			if firstRow:
				firstRow = False
				continue
			
			#Date,Open,High,Low,Close,Volume,Adj Close
			data.append(tuple([self._parsedatestring(row[0]), float(row[4])]))
			
		f.close()
		return data

	def symbol_get_volumes(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'volume')
		"""
		
		data = []
		filename = self.download2csv(symbol_name, mindate, maxdate)
		f = open(filename, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		firstRow = True
		for row in reader:
			
			# skip field names row
			if firstRow:
				firstRow = False
				continue
			
			#Date,Open,High,Low,Close,Volume,Adj Close
			data.append(tuple([self._parsedatestring(row[0]), float(row[5])]))
			
		f.close()
		return data
		
	def symbol_get_ochlv(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'open', 'close', 'high', 'low')
		"""
		
		data = []
		filename = self.download2csv(symbol_name, mindate, maxdate)
		f = open(filename, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		firstRow = True
		for row in reader:
			
			# skip field names row
			if firstRow:
				firstRow = False
				continue
			
			#Date,Open,High,Low,Close,Volume,Adj Close
			data.append(tuple([self._parsedatestring(row[0]), 
				float(row[1]),
				float(row[2]),
				float(row[3]),
				float(row[4]),
				float(row[5])]))
			
		f.close()
		return data


	def symbol_get_maxdate(self, symbol_name):
		"""Get the latest date available for the given symbol.
		
		Returns: datetime object
		"""

		datelist = []
		filename = self.download2csv(symbol_name)
		f = open(filename, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		firstRow = True
		for row in reader:
			
			# skip field names row
			if firstRow:
				firstRow = False
				continue
			
			#Date,Open,High,Low,Close,Volume,Adj Close
			datelist.append(row[0])
			
		f.close()
		
		lastdate = datelist[0] # results are order by date desc
		datetime_obj = datetime.datetime.strptime(lastdate, '%Y-%m-%d')

		return datetime_obj
		

	def close(self):
		"""Just to stay consistent with LocalSource"""
		pass
		

	def download2csv(self, symbol_name, mindate=None, maxdate=None):
		"""Download data for given symbol to local CSV file. The CSV
		file contains field names in the first row.
		
		The CSV file contains the following fields:
		
			Date,Open,High,Low,Close,Volume,Adj Close
		
		Return a filename, pointing to the temporary local file data has
		been downloaded to.
		"""

		if not self.symbol_exists(symbol_name):
			raise Exception("Symbol {0} does not exists".format(symbol_name))
			
		url = self._get_url(symbol_name, mindate, maxdate, True)
		return urllib.urlretrieve(url)[0]
		

	def symbol_exists(self, symbol_name):
		"""Check if given symbol exists in yahoo database.
		
		Return True / False.
		"""
		
		url = URL_CHECK_EXISTENCE.format(symbol_name)
		response = urllib.urlopen(url)
		html = response.read()
		
		if "There are no results for the given search term" in html:
			self.logger.info("Symbol {0} not found in remote database".format(symbol_name))
			return False
		else:
			self.logger.info("Symbol {0} found in remote database".format(symbol_name))
			return True


	def get_index_components(self, index_name):
		"""Given a Yahoo symbol that points to an index, download a list
		of all the single stocks ( that is symbols ) that compose the
		index.
		
		Parameters:
		
			index_name :: a string for the Yahoo symbol of the index
			
		Returns a list of symbol names.
		"""
		pass


class LocalSource(Source):
	
	def __init__(self, path):
		"""Open database if it already exists; initialize a new one
		otherwise."""
		
		super(LocalSource, self).__init__()
		
		initialize = False
		if not os.path.isfile(path):
			self.logger.info("Initializing new local database.")
			initialize = True

		self.conn = sqlite3.connect(path)
		self.conn.text_factory = str # https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.text_factory
		###self.conn.row_factory = sqlite3.Row # rows can be now accessed both by index (like tuples) and case-insensitively by name
		
		if initialize: self.database_initialize()
		
		try:
			cur = self.conn.cursor()
			cur.execute("select * from DAT_EoD limit 1")
		except Exception, ex:
			self.log.error(traceback.format_exc())
			raise Exception("Table DAT_EoD not found. Are you sure this is a proper data source ?")


	def DELETE_eod_exists(self, symbol_name):
		"""Check if given symbol exists in local EoD table, that is to
		say that we check if exists at least one row of data for the 
		given symbol.
		
		We do not check existence of given symbol in DAT_Symbol table.
		
		Return True / False.
		"""
		
		sql = "select * from DAT_EoD where symbol = '{0}'".format(symbol_name)
		
		cur = self.conn.cursor()
		cur.execute (sql)
		row = cur.fetchone()
		cur.close()
		
		if row:
			return True
		else:
			return False
		

	def _query(self, symbol, columns=[], mindate=None, maxdate=None):
		"""
		Parameters:
		
			symbol : the name of the symbol using Yahoo convention (ie: SPM.MI)
			columns : a list of column names
			mindate : a string in the format '%Y-%m-%d'
			maxdate : a string in the format '%Y-%m-%d'
		"""
		
		sql = 'select *'
		if len(columns) > 0:
			sql = 'select '
			firstloop = True
			for column in columns:
				
				if firstloop:
					firstloop = False
				else:
					column = ", " + column
				
				sql += column
		
		sql += " from DAT_EoD where symbol = '{0}'".format(symbol)
		
		# FIXME: use `date` field instead of `date_STR`
		
		if mindate:
			sql = sql + " and date_STR >= strftime('%Y-%m-%d', '{0}')".format(mindate)
		
		if maxdate:
			sql = sql + " and date_STR >= strftime('%Y-%m-%d', '{0}')".format(maxdate)
		
		cur = self.conn.cursor()
		cur.execute (sql)
		rows = cur.fetchall()
		cur.close()
	
		if len(rows) == 0: 
			raise DataError("No data can be retrieved for the given symbol.")
	
		return rows
		

	def close(self):
		self.conn.close()


	def symbol_get_maxdate(self, symbol_name):
		"""Get the most recent date available for the given symbol.
		
		Returns: a datetime object.
		"""
		
		# FIXME: use `date` field instead of `date_STR`
		
		cur = self.conn.cursor()
		cur.execute("select date_STR from DAT_EoD where symbol = '{0}'"
			" order by date_STR desc limit 1".format(symbol_name))

		row = cur.fetchone()
		cur.close()
		
		if row:
			maxdate_str = row[0]
			maxdate = datetime.datetime.strptime(str(maxdate_str), "%Y-%m-%d")
		else:
			maxdate = None
		
		return maxdate		
		
			
	def symbol_get_all(self):
		"""Return all the symbols stored in the DAT_Symbol table.
		We also retrieve the last EoD date, if present"""
		
		cur = self.conn.cursor()
		# cur.execute("select code, descr from DAT_symbol order by code")
		cur.execute("select sym.code, sym.descr, eod.maxdate from DAT_Symbol sym "\
			"left join ( select symbol, date(max(date), 'unixepoch') as maxdate "\
			"from DAT_EoD group by symbol ) eod on sym.code = eod.symbol")

		rows = cur.fetchall()
		cur.close()
		
		return rows
		
	
	def symbol_get_all_loaded(self):
		"""Return all the symbols present in the local database, with
		related most recent date.
		
		These are the symbols for which we have data, not the 
		symbols present in the DAT_Symbol table."""
		
		cur = self.conn.cursor()
		#~ cur.execute("select symbol, strftime('%Y-%m-%d', max(date)) as maxDate from DAT_EoD group by symbol order by symbol")
		cur.execute("select symbol, date(max(date), 'unixepoch') as maxDate from DAT_EoD group by symbol order by symbol")

		rows = cur.fetchall()
		cur.close()
		
		symbols = []
		for row in rows:
			symbols.append([row[0], row[1]])

		return symbols
		
		
	def symbol_get_closings(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'close')
		"""
		return self._query(symbol_name, ['date', 'close'], mindate, maxdate)

	def symbol_get_volumes(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'volume')
		"""
		return self._query(symbol_name, ['date', 'volume'], mindate, maxdate)
		
	def symbol_get_ochlv(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'open', 'close', 'high', 'low', 'volume')
		"""
		return self._query(symbol_name, ['date', 'open', 'close', 'high', 'low', 'volume'], mindate, maxdate)
	
	def symbol_exists(self, symbolName):
		"""Check for symbol existence"""
		
		sql = "select * from DAT_Symbol where code = '{0}'".format(symbolName)
		
		cur = self.conn.cursor()
		cur.execute (sql)
		row = cur.fetchone()
		cur.close()
		
		if row:
			return True
		else:
			return False
		
	
	def symbol_search(self, string):
		"""Search database for a symbol with symbol name """
		raise Exception("Not implemented yet")
	
	def symbol_add(self, symbol_name, symbol_descr=None):
		"""Add given symbol to database"""
		
		if OnlineSource().symbol_exists(symbol_name):
			cur = self.conn.cursor()
			cur.execute('INSERT INTO `DAT_Symbol` (`code`, `descr`)'
				' VALUES (?,?)', (symbol_name, symbol_descr))
			self.conn.commit()
		else:
			raise Exception("Given symbol does not exists")
	
	
	def symbol_refresh_eod(self, symbol_name):
		
		self.logger.info("Refreshing symbol <{0}>".format(symbol_name))
		
		# check if symbol exists
		if not self.symbol_exists(symbol_name):
			raise Exception("Given symbol does not exist.")
		
		maxdate = self.symbol_get_maxdate(symbol_name)
		if maxdate == None:
			self.logger.info("No EoD data available for given symbol")
			maxdate = datetime.datetime(1900,1,1)
		else:
			self.logger.info("Max date available: {0}".format(maxdate.strftime("%Y-%m-%d")))
			
			# check if it's up to date
			delta = datetime.datetime.today() - maxdate
			if delta.days <= 2:
				self.logger.info("Already up to date, skipping symbol refresh.")
				return
				
			maxdate = maxdate + datetime.timedelta(days=1) # start downloading from the next day
			self.logger.info("Computed max date: {0}".format(maxdate.strftime("%Y-%m-%d")))
		
		filename = OnlineSource().download2csv(symbol_name, mindate=maxdate)
		self.eod_load_from_csv(symbol_name, filename)
		
		
	def symbol_all_refresh_eod(self):
		"""Refresh EoD data for all the symbols stored in the local database"""
		
		symbols = self._get_all_symbols()
		self.logger.info("Found {0} total symbols in database".format(len(symbols)))
		
		counter = 1
		for symbol in symbols:
			self.logger.info("Refreshing symbol {0}/{1}".format(counter, len(symbols)))
			self.refresh(symbol)
			counter += 1
		
		
	def eod_load_from_csv(self, symbol_name, filename):
		"""Load EoD data of given symbol from the CSV file.
		
		Usually, the CSV you load the data from is the one that you 
		create using yahoo.OnlineSource.download2csv method.
		"""
		
		f = open(filename, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		cur = self.conn.cursor()

		firstRow = True
		for row in reader:
			
			# skip first row
			if firstRow:
				firstRow = False
				continue
			
			row.insert(0, symbol_name) # insert symbol
			cur.execute('INSERT INTO `DAT_EoD` (`symbol`, `date_STR`,'
				'`open`,`high`,`low`,`close`,`volume`,`adj_close`) VALUES (?,?,?,?,?,?,?,?)', row)
				
		f.close()
		
		### now update the field `date_UNIX`
		cur.execute("update DAT_EoD set date = strftime('%s', `date_STR`)")
		
		self.conn.commit()
		
		
	def symbol_load_from_csv(self, filename, index_name, index_descr=None):
		"""Parse a CSV file, containing a list of symbols, to populate
		DAT_symbol table. Loaded symbols will be linked to a newly 
		created index ( DAT_index table ).
		
		The CSV file is supposed to be UTF-8 encoded.
		
		The CSV file, with tab separated data, should at least contain 
		two columns: the first one being the Yahoo symbol and the second 
		a description of the symbol.
		
		For the time being, you have to manually create the CSV. My 
		suggestion is to make some copying&pasting from a page like this 
		one:
		
			http://finance.yahoo.com/q/cp?s=^DJI+Components
		
		Parameters:
			
			<index_name> :: short name for the index ( ie: 'FTSEMIB' )
			<index_descr> :: an optional, longer text describing the index
			
		"""
		
		self.logger.info("Loading index {0}".format(index_name))
		
		try:

			cur = self.conn.cursor()

			cur.execute("insert into DAT_index (`code`, `descr`)"
				" values ('{0}', '{1}')".format(index_name, index_descr))
			
			inputFile = open(filename, 'rb')
			reader = csv.reader(inputFile, delimiter='\t')

			for row in reader:
				
				self.logger.debug(row)
				
				if row == []:
					continue
				
				if row[0][0] == '#':
					continue
				
				# symbol may be already present, no error in that case
				cur.execute('INSERT OR IGNORE INTO `DAT_symbol` (`code`, `descr`) '
					'VALUES (?,?)', [row[0], row[1].decode('utf-8')])

				cur.execute('INSERT OR IGNORE INTO DAT_index_symbol ( `index`, `symbol`) '
					'VALUES (?,?)', [index_name, row[0]])
					
			inputFile.close()
			
		except Exception, ex:
			self.logger.error(traceback.format_exc())
			self.conn.rollback()
			raise Exception("Cannot parse file {0}".format(filename))
		
		self.conn.commit()
		
		
	def database_initialize(self):
		
		ddl = open('create_schema.sql', 'r').read()
		cur = self.conn.cursor()
		cur.executescript(ddl)
		self.conn.commit()
		cur.close()
		
	
	def symbol_load_eod(self, symbol_name):
		"""Download data from Yahoo servers to a local file, then load 
		these data into local database.
		"""
		
		self.logger.info("Loading data for symbol {0}".format(symbol_name))
		
		self.delete(symbol_name)	# clean database
		filename = OnlineSource().download2csv(symbol_name)
		self._load_from_csv(symbol_name, filename)
		
		
	def symbol_all_load_eod(self):
		"""Load all historical prices for symbols included in table 
		DAT_symbol."""
		
		symbols = self.symbol_get_all()
		self.logger.info("Found {0} total symbols in database".format(len(symbols)))
		
		counter = 1
		for symbol in symbols:
			self.logger.info("Loading symbol {0}/{1}".format(counter, len(symbols)))
			self.symbol_load_eod(symbol)
			counter += 1
		

	def DELETE_load_all_from_index(self, index_name):
		"""Table DAT_index_symbol links an index with many symbols.
		
		Given and index, this method loads all the linked symbols.
		"""
		
		cur = self.conn.cursor()
		cur.execute("select is.symbol from DAT_index i "
			"inner join DAT_index_symbol is on is.index = i.code "
			"where i.code = ?", index_name)

		rows = cur.fetchall()
		self.logger.info("Found {0} total symbols in given index".format(len(rows)))
		cur.close()
		
		counter = 1
		for row in rows:
			self.logger.info("Loading symbol {0}/{1}".format(counter, len(rows)))
			self.symbol_load_eod(row[0])
			counter += 1


	def symbol_delete(self, symbol):
	
		cur = self.conn.cursor()
		cur.execute('delete from DAT_EoD where symbol = ''?''', (symbol,) )
		self.conn.commit()
		
	
	def reset(self):
		
		cur = self._get_cursor()
		
		try:
			cur.execute('truncate table DAT_EoD')
			
		except Exception, ex:
			
			self.log.error(traceback.format_exc())
			self.logger.error("Cannot truncate table DAT_EoD")
		
