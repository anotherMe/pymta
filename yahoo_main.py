#!/usr/bin/python

"""Helper script used to automate basic operation on a yahoo.LocalSource
"""

import argparse
import yahoo
import sys

class MainApp:
	
	def __init__(self, path):
		
		self.source = yahoo.LocalSource(path)
		#~ source._load_index_from_csv("FTSEMIB.MI", "data/FTSEMIB.MI.csv", "FTSE MIB")
		#~ source._load_index_from_csv("^DJI", "data/DJIA.csv", "Dow Jones Industrial Average")
		#~ source.refresh_all()
		#~ source.refresh('BA')
		sym = self.source._get_all_symbols()
		print "Got {0} symbols in database (table DAT_symbol)".format(len(sym))

	def info(self, symbol):
		
		raise Exception("Not implemented yet")

	def refresh(self, symbol):
		
		if symbol.lower() == "all":
			self.source.refresh_all()
		else:
			self.source.refresh(symbol.upper())
		
	def load(self, symbol):
		
		if symbol.lower() == "all":
			self.source.load_all()
		else:
			self.source.load(symbol.upper())
		
	def info_index(self, index):
		
		raise Exception("Not implemented yet")
				
	def refresh_index(self, index):
		
		raise Exception("Not implemented yet")
		
	def load_index(self, symbol):
		
		raise Exception("Not implemented yet")		


if __name__=='__main__':

	parser = argparse.ArgumentParser(description='A simple, command line interface, to pymta LocalSource')
	parser.add_argument('source', help='path to the LocalSource database')
	parser.add_argument('-s', '--symbol', help='a single symbol string, according to yahoo'
		' convention (ie: "SPM.MI") or "all" if you want to process all the symbols in the database')
	parser.add_argument('-ix', '--index', help='specify an index string (ie: "FTSEMIB.MI") to work with all the related symbols')
	parser.add_argument('-i', '--info', action="store_true", help='print some info about given symbol')
	parser.add_argument('-r', '--refresh', action="store_true", help='refresh given symbol')
	parser.add_argument('-l', '--load', action="store_true", help='load or re-load given symbol into database')
	args = parser.parse_args()
	
	app = MainApp(args.source)
	
	if (args.symbol == None and args.index == None):
		print "You cannot specify a symbol and an index at the same time."
		sys.exit(0)


	if args.index:
		
		if args.info:
			app.info(args.index)
		elif args.refresh:
			app.refresh(args.index)
		elif args.load:
			app.load(args.index)
	
	else:
		
		if args.info:
			app.info(args.symbol)
		elif args.refresh:
			app.refresh(args.symbol)
		elif args.load:
			app.load(args.symbol)


