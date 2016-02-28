#!/usr/bin/python

"""Helper script used to automate basic operation on a yahoo.LocalSource
"""

import argparse
import yahoo
import sys
import os

import pdb


class MainApp:
	
	def __init__(self, path):
		
		self.source = yahoo.LocalSource(path)
		self.pageMain()

	def outLog(self, severity, msg):
		print ""
		print("{0} - {1}".format(severity, msg))
		print ""
		raw_input("(Press ENTER to continue)")

	def outPrint(self, msg):
		print ""
		print("{0}".format(msg))
		print ""
		raw_input("(Press ENTER to continue)")
		
	def outClearScreen(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	def outChoiceList(self, choiceList):
		
		print "Type:"
		print ""
		for choice in choiceList:
			print "{0} :: {1}".format(choice[0], choice[1])
		print ""	
		

	def pageMain(self):
	
		self.outClearScreen()

		cl = []
		cl.append(["sym", "to manage symbols stored in local database"])
		cl.append(["eod", "to load/refresh EndOfDay data for stored symbols"])
		cl.append(["plot", "to load/refresh EndOfDay data for stored symbols"])
		cl.append(["quit", "to exit program"])
		self.outChoiceList(cl)
		
		while 1==1:
			s = raw_input(">")
			args = s.split(' ')
			
			command = args[0].strip().lower()
			if command == 'sym' or command == 's':
				self.pageManageSymbols()
			elif command == 'eod' or command == 'e':
				self.pageManageEoDs()
			elif command == 'plot' or command == 'p':
				self.pagePlot()
			elif command == 'quit' or command == 'q':
				self.cmdQuit()
			else:
				pageMain()
				
		
	def pageManageSymbols(self):
		
		self.outClearScreen()

		cl = []
		cl.append(["add", "to add a new symbol to local database"])
		cl.append(["list", "to list all currently stored symbols"])
		#~ cl.append(["index", "to load a list of symbols from a CSV file"])
		cl.append(["search", "to search through currently stored symbols"])
		cl.append(["back", "to go back one page"])
		self.outChoiceList(cl)

		while 1==1:
			s = raw_input(">")
			args = s.split(' ')
			
			command = args[0].strip().lower()
			if command == 'add' or command == 'a':
				self.cmdSymbolAdd(args[1:])
			#~ elif command == 'index' or command == 'i':
				#~ self.cmdToDo(args[1:])
			elif command == 'list' or command == 'l':
				self.cmdSymbolList(args[1:])
			elif command == 'back' or command == 'b':
				self.pageMain()
			else:
				self.pageManageSymbols()
				
		
		
	def pageManageEoDs(self):

		allsymbols = self.source.get_all_symbols()
		if allsymbols.length == 0:
			self.outPrint("You should load some symbols first")
			self.pageMain()
					
		self.outClearScreen()
		
		cl = []
		cl.append(["info", "get info on given symbol"])
		self.outChoiceList(cl)

		while 1==1:
			s = raw_input(">")
			args = s.split(' ')
			
			command = args[0].strip().lower()
			if command == 'help' or command == 'h':
				self.cmdHelp(args[1:])
			elif command == 'list' or command == 'l':
				self.cmdList(args[1:])
			elif command == 'search' or command == 's':
				self.cmdList(args[1:])
			elif command == 'load':
				self.cmdLoad(args[1:])
			elif command == 'refresh':
				self.cmdRefresh(args[1:])
			elif command == 'clear' or command == 'c':
				self.outClearScreen()
			elif command == 'quit' or command == 'q':
				self.cmdQuit()
			else:
				self.pageManageEoDs()
				
				
	def pagePlot(self):
		
		allsymbols = self.source.get_all_symbols()
		if allsymbols.length == 0:
			self.outPrint("You should load some symbols first")
			self.pageMain()
					
		self.outClearScreen()
		
		
				
		
	def cmdSymbolAdd(self, args):
		
		sym = args[0].upper()
		
		if len(args) == 0:
			self.outPrint("You should provide an argument to <add>")
			return
		
		if self.source.symbol_exists(sym):
			self.outPrint("A symbol named {0} already exists".format(sym))
			return

		print "Please provide a description for the new symbol"
		descr = raw_input()
		
		try:
			self.source.symbol_add(sym, descr)
		except Exception, ex:
			self.outLog('ERROR', ex.message)
			return
			
			
		
	def cmdSymbolSearch(self, args):
		
		if args.length == 0:
			self.outPrint("You should provide at least one argument")
			self.pageManageSymbols()
	
	
	def cmdSymbolList(self, args):
		
		try:
			allsymbols = self.source.symbol_get_all()
		except Exception, ex:
			self.outLog("ERROR", ex.message)
			return
		
		if len(allsymbols) == 0:
			self.outPrint("No symbols stored in database")
			return
		
		for symbol in allsymbols:
			print "{0} last update on {1}".format(symbol[0], symbol[1])
		print("")
		raw_input("Press Enter to continue...")

		
		
	def cmdEodRefresh(self, args):
		
		try:
			if args[0].lower() == "all":
				self.source.refresh_all()
			else:
				self.source.refresh(args[0].upper())
		except Exception, ex:
			self.outLog("ERROR", ex.message)
		
		
	def cmdEodLoad(self, args):

		try:
			if args[0].lower() == "all":
				self.source.load_all()
			else:
				self.source.load(args[0].upper())
		
		except Exception, ex:
			self.outLog("ERROR", ex.message)
		
	def cmdToDo(self, args):
		raise Exception("Not yet implemented")
		
	def cmdQuit(self):
		sys.exit(0)

		

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='A simple, command line interface, to pymta LocalSource')
	parser.add_argument('source', help='Open given database file or create a new one if not existing')
	args = parser.parse_args()	
	app = MainApp(args.source)
	
