#!/usr/bin/python

"""Helper script used to automate basic operation on a yahoo.LocalSource
"""

import argparse
import yahoo
import sys
import os

class MainApp:
	
	def __init__(self, path):
		
		self.source = yahoo.LocalSource(path)
		#~ sym = self.source._get_all_symbols()
		#~ print "Got {0} symbols in database (table DAT_symbol)".format(len(sym))
		self.mainPage()

	def log(self, severity, msg):
		print("{0} - {1}".format(severity, msg))

	def mainPage(self):
		
		self.clearScreen()
		print("Type <help> for a list of available commands")

		while 1==1:
			s = raw_input(">")
			args = s.split(' ')
			
			command = args[0].strip().lower()
			if command == 'help':
				self.cmdHelp(args[1:])
			elif command == 'list':
				self.cmdList(args[1:])
			elif command == 'load':
				self.cmdLoad(args[1:])
			elif command == 'refresh':
				self.cmdRefresh(args[1:])
			elif command == 'quit':
				break
			else:
				print ("Unrecognized command")
		
	
	def cmdList(self, args):
		
		try:
			allsymbols = self.source._get_all_loaded_symbols()
		except Exception, ex:
			self.log("ERROR", "Unable to retrieve list of symbols")
			return
		
		for symbol in allsymbols:
			print "{0} last update on {1}".format(symbol[0], symbol[1])
		print("")
			
		s = raw_input("Press Enter")
		self.mainPage()
	
	
	def cmdHelp(self, args):
		
		self.clearScreen()
		print("Available commands:")
		print("")
		print("load - load symbol data from Yahoo servers into local database")
		print("refresh - refresh symbol data from Yahoo servers into local database")
		print("list - list all available symbols in local database")
		print("help - print this help")
		print("quit - quit this app")
		print("")
		
		
	def cmdRefresh(self, symbol):
		
		try:
			if args[0].lower() == "all":
				self.source.refresh_all()
			else:
				self.source.refresh(args[0].upper())
		except Exception, ex:
			self.log("ERROR", "Cannot refresh given symbol")
		
	def cmdLoad(self, args):

		try:
			if args[0].lower() == "all":
				self.source.load_all()
			else:
				self.source.load(args[0].upper())
		
		except Exception, ex:
			self.log("ERROR", "Cannot load given symbol")


	def clearScreen(self):
		
		os.system('cls' if os.name == 'nt' else 'clear')
		

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
	
