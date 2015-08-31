#!/usr/bin/env python2

import logging as log
log.basicConfig(filename='yahoo.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import sqlite3
import urllib
import csv
import datetime as dt
import os

import pdb


URL_CHECK_EXISTENCE = "https://finance.yahoo.com/q?s={0}"
URL_CSV_DOWNLOAD = "http://real-chart.finance.yahoo.com/table.csv"


class DataError(Exception):
	"""Raised when there's no data available for the requested symbol.
	"""
	
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)
		

class _Symbol:
	"""
	Constructor takes a data source (LocalSource or OnlineSource) object 
	and a symbol name.
	
	You're not supposed to instantiate this class. Use get_symbol
	method instead.
	"""
	
	def __init__(self, datasource, symbol_name, mindate = None, maxdate = None):
		"""Parameters:
			
			datasource :: a valid yahoo.LocalSource or yahoo.OnlineSource
			symbol_name :: the Yahoo symbol used to identify the stock
			mindate :: from date
			maxdate :: to date
			
		"""
		
		self.name = symbol_name
		self.source = datasource
		
		# just to save some typing, define mindate and maxdate as instance properties
		self.mindate = mindate
		self.maxdate = maxdate


	def get_data(self, columns=[], mindate = None, maxdate = None):
		
		if mindate:
			self.mindate = mindate
			
		if maxdate:
			self.maxdate = maxdate
		
		return self.source._query(self.name, columns, self.mindate, self.maxdate)


class OnlineSource():
	
	def __init__(self):
		pass

	def get_symbol(self, symbol_name):
		symbol = _Symbol(self, symbol_name)
		return symbol

	def _query(self, symbol, columns=[], mindate=None, maxdate=None):
		"""Returns a list of tuples."""
		
		raise Exception("Not implemented yet")

	def get_maxdate(self, symbol):
		"""Returns most recent date available for the given symbol."""
		
		raise Exception("Not implemented yet")

	def close(self):
		"""Just to maintain consistency with LocalSource"""
		pass
		

	def download2csv(self, symbol, mindate=None, maxdate=None):
		"""Download data for given symbol to local CSV file. 
		
		Return a tuple (filename, headers) where filename is the local file 
		name.
		"""
		
		url = URL_CSV_DOWNLOAD + "?s={0}".format(symbol)
		if maxdate != None:
			url += "&a={0}&b={1}&c={2}".format(maxdate.month - 1, maxdate.day, maxdate.year)
		if mindate != None:
			url += "&d={0}&e={1}&f={2}".format(mindate.month - 1, mindate.day, mindate.year)
		url += "&g=d" # daily data
		url += "&ignore=.csv"
		log.debug(url)
		return urllib.urlretrieve (url)
		

	def exists(self, symbol):
		"""Check if given symbol exists in yahoo database.
		
		Return True / False.
		"""
		
		url = URL_CHECK_EXISTENCE.format(symbol)
		response = urllib.urlopen(url)
		html = response.read()
		
		if "There are no results for the given search term" in html:
			log.info("Symbol not found")
			return False
		else:
			log.info("Symbol found")
			return True


class LocalSource():
	
	def __init__(self, path):
		"""Open database if it already exists; initialize a new one
		otherwise."""
		
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


	def get_symbol(self, symbol_name):
		symbol = _Symbol(self, symbol_name)
		return symbol


	def exists(self, symbol):
		"""Check if given symbol exists in local EoD table, that is to
		say that we check if exists at least one row of data for the 
		given symbol.
		
		We do not check existence of given symbol in DAT_Symbol table.
		
		Return True / False.
		"""
		
		sql = "select * from DAT_EoD where symbol = '{0}'".format(symbol)
		
		cur = self.conn.cursor()
		cur.execute (sql)
		row = cur.fetchone()
		cur.close()
		
		if row:
			return True
		else:
			return False


	def _query(self, symbol, columns=[], mindate=None, maxdate=None):
		"""Returns a list of tuples."""
		
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
		
		if mindate:
			sql = sql + " and date >= strftime('%Y-%m-%d', '{0}')".format(mindate)
		
		if maxdate:
			sql = sql + " and date >= strftime('%Y-%m-%d', '{0}')".format(maxdate)
		
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
		"""Returns most recent date available for the given symbol."""
		
		cur = self.conn.cursor()
		cur.execute("select date from DAT_EoD where symbol = '{0}'"
			" order by date_UNIX desc limit 1".format(symbol_name))

		row = cur.fetchone()
		maxdate_str = row[0]
		cur.close()
		
		maxdate = dt.datetime.strptime(str(maxdate_str), "%Y-%m-%d")
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
			cur.execute('INSERT INTO `DAT_EoD` (`symbol`, `date`,'
				'`open`,`high`,`low`,`close`,`volume`,`adj_close`) VALUES (?,?,?,?,?,?,?,?)', row)
				
		f.close()
		
		### now update the field `date_UNIX`
		cur = self.conn.cursor()
		cur.execute("update DAT_EoD set date_UNIX = strftime('%s', `date`)")
		
		self.conn.commit()
		
		
	def _initialize(self):
		
		ddl = open('create_schema.sql', 'r').read()
		cur = self.conn.cursor()
		cur.executescript(ddl)
		self.conn.commit()
		cur.close()
		
	
	def load(self, symbol):
		"""Download and reload on the database all the data for the 
		given symbol.
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
