#!/usr/bin/env python2

import logging as log
log.basicConfig(filename='yahoo.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import sqlite3
import urllib
import csv
import datetime
import os
import data

import pdb


URL_CHECK_EXISTENCE = "https://finance.yahoo.com/q?s={0}"


class DataError(Exception):
	"""Raised when there's no data available for the requested symbol.
	"""
	
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		
		
class OnlineSource(data.Source):
	
	def __init__(self):
		
		super(OnlineSource, self).__init__()

	def _parsedatestring(self, inputdate):
		"""Parameters:
		
			inputdate: a string representing a date in the format '%Y-%m-%d'
			
		Returns an integer, representing the number of seconds since Epoch
		"""
		
		datetime_obj = datetime.datetime.strptime(inputdate, '%Y-%m-%d')
		return int(datetime_obj.strftime('%s'))

	def _get_closings(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'close')
		"""
		
		data = []
		fh = self.download2csv(symbol_name, mindate, maxdate)
		f = open(fh[0], 'rb')
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

	def _get_volumes(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'volume')
		"""
		
		data = []
		fh = self.download2csv(symbol_name, mindate, maxdate)
		f = open(fh[0], 'rb')
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
		
	def _get_ochlv(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'open', 'close', 'high', 'low')
		"""
		
		data = []
		fh = self.download2csv(symbol_name, mindate, maxdate)
		f = open(fh[0], 'rb')
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


	def get_maxdate(self, symbol_name):
		"""Get the latest date available for the given symbol.
		
		Returns: datetime object
		"""
		
		datelist = []
		fh = self.download2csv(symbol_name)
		f = open(fh[0], 'rb')
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
		
		Return a tuple (filename, headers) where filename is the local file 
		name.
		"""

		if not self.exists(symbol_name):
			raise Exception("Symbol {0} does not exists".format(symbol_name))
			
		url = self._get_url(symbol_name, mindate, maxdate, True)
		return urllib.urlretrieve (url)
		

	def exists(self, symbol_name):
		"""Check if given symbol exists in yahoo database.
		
		Return True / False.
		"""
		
		url = URL_CHECK_EXISTENCE.format(symbol_name)
		response = urllib.urlopen(url)
		html = response.read()
		
		if "There are no results for the given search term" in html:
			log.info("Symbol not found")
			return False
		else:
			log.info("Symbol found")
			return True


class LocalSource(data.Source):
	
	def __init__(self, path):
		"""Open database if it already exists; initialize a new one
		otherwise."""
		
		super(LocalSource, self).__init__()
		
		initialize = False
		if not os.path.isfile(path):
			log.info("File not exists yet, initializing a new local database.")
			initialize = True

		self.conn = sqlite3.connect(path)
		###self.conn.row_factory = sqlite3.Row # rows can be now accessed both by index (like tuples) and case-insensitively by name
		
		if initialize: self._initialize()
		
		try:
			cur = self.conn.cursor()
			cur.execute("select * from DAT_EoD limit 1")
		except Exception, ex:
			raise Exception("Table DAT_EoD not found. Are you sure this is a proper data source ?")


	def exists(self, symbol_name):
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


	def get_maxdate(self, symbol_name):
		"""Get the most recent date available for the given symbol.
		
		Returns a datetime object.
		"""
		
		# FIXME: use `date` field instead of `date_STR`
		
		cur = self.conn.cursor()
		cur.execute("select date_STR from DAT_EoD where symbol = '{0}'"
			" order by date_STR desc limit 1".format(symbol_name))

		row = cur.fetchone()
		maxdate_str = row[0]
		cur.close()
		
		maxdate = datetime.datetime.strptime(str(maxdate_str), "%Y-%m-%d")
		return maxdate
		
		
	def _get_all_symbols(self):
		"""Return all the symbols present in the local database.
		
		These are not the symbols for which we have data, just the 
		symbols present in the DAT_Symbol table."""
		
		cur = self.conn.cursor()
		cur.execute("select symbol from DAT_symbol order by symbol")

		rows = cur.fetchall()
		cur.close()
		
		symbols = []
		for row in rows:
			symbols.append(row[0])

		return symbols
		
	def _get_closings(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'close')
		"""
		return self._query(symbol_name, ['date', 'close'], mindate, maxdate)

	def _get_volumes(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'volume')
		"""
		return self._query(symbol_name, ['date', 'volume'], mindate, maxdate)
		
	def _get_ochlv(self, symbol_name, mindate=None, maxdate=None):
		"""Returns: a list of tuple ('date', 'open', 'close', 'high', 'low', 'volume')
		"""
		return self._query(symbol_name, ['date', 'open', 'close', 'high', 'low', 'volume'], mindate, maxdate)
	
	
	def refresh(self, symbol):
		
		log.info("Refreshing symbol <{0}>".format(symbol))
		
		# if symbol not exists, download all data and exit
		if not self.exists(symbol):
			self.load(symbol)
		
		
		# check if it's up to date
		maxdate = self.get_maxdate(symbol)		
		delta = dt.datetime.today() - maxdate
		
		if delta.days <= 2:
			return
			
		maxdate = maxdate + dt.timedelta(days=1) # start downloading from the next day
		fh = self._download(symbol, maxdate=maxdate)
		self._load(symbol, fh[0])
		
		
	def refresh_all(self):
		
		symbols = self._get_all_symbols()
		
		for symbol in symbols:
			self.refresh(symbol)
		
		
	def _load_from_csv(self, symbol, filename):
		
		f = open(filename, 'rb')
		reader = csv.reader(f, delimiter=',')
		
		cur = self.conn.cursor()

		firstRow = True
		for row in reader:
			
			# skip first row
			if firstRow:
				firstRow = False
				continue
			
			row.insert(0, symbol) # insert symbol
			cur.execute('INSERT INTO `DAT_EoD` (`symbol`, `date_STR`,'
				'`open`,`high`,`low`,`close`,`volume`,`adj_close`) VALUES (?,?,?,?,?,?,?,?)', row)
				
		f.close()
		
		### now update the field `date_UNIX`
		cur = self.conn.cursor()
		cur.execute("update DAT_EoD set date = strftime('%s', `date_STR`)")
		
		self.conn.commit()
		
		
	def _initialize(self):
		
		ddl = open('create_schema.sql', 'r').read()
		cur = self.conn.cursor()
		cur.executescript(ddl)
		self.conn.commit()
		cur.close()
		
	
	def load(self, symbol):
		"""Download and reload onto the local database all the data for 
		the given symbol.
		"""
		
		self._delete(symbol)	# clean database
		fh = OnlineSource().download2csv(symbol)
		self._load_from_csv(symbol, fh[0])
		
		
	def load_all(self):
		"""Load all historical prices for symbols included in table 
		DAT_symbol."""
		
		symbols = self._get_all_symbols()
		for symbol in symbols:
			self.load(symbol)
		

	def _delete(self, symbol):
	
		cur = self.conn.cursor()
		cur.execute('delete from DAT_EoD where symbol = ''?''', (symbol,) )
		self.conn.commit()
		
	
	def reset(self):
		
		cur = self._get_cursor()
		
		try:
			cur.execute('truncate table DAT_EoD')
			
		except Exception, ex:
			
			log.error("Cannot truncate table DAT_EoD")
			log.error(ex)
