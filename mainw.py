#!/usr/bin/env python

import sys
import traceback
import logging
import Tkinter as tk
import tkFileDialog
import ttk
import tklib.console as tkcon
import tklib.symbol as tksym
import tklib.plot as tkplot
import yahoo
import pdb


VERSION="0.0.4"


DEFAULT_DATABASE_PATH="/home/marco/lab/pymta/devdb.db3"
#DEFAULT_DATABASE_PATH="C:/mg/lab/pymta/devdb.db3"

class Application():

	
	def __init__(self, root):

		logging.basicConfig(filename='mainw.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
		self.log = logging.getLogger(__name__)
		
		self.root = root
		self.source = None
		
		self.root.title("pymta tkInterface {0}".format(VERSION))

		# menu bar
		menubar = tk.Menu(self.root)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="New", command=self.database_new)
		filemenu.add_command(label="Open", command=self.database_open)
		filemenu.add_command(label="Exit", command=self.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		toolsmenu = tk.Menu(menubar, tearoff=0)
		toolsmenu.add_command(label="Load symbols from file", command=self.symbol_load_from_file)
		menubar.add_cascade(label="Tools", menu=toolsmenu)
		self.root.config(menu=menubar)
		
		# notebook
		notebook = ttk.Notebook(self.root)
		notebook.pack(fill=tk.BOTH, expand=1)
		
		# tabs
		manageSymbolsTab = tk.Frame(notebook)
		notebook.add(manageSymbolsTab, text="Manage symbols")
		plotTab = tk.Frame(notebook)
		notebook.add(plotTab, text="Plot")
		
		# show console window
		self.con = tkcon.Window(self.root)
		
		# manage symbols tab - symbols list
		self.symbolsList = tksym.SymbolList(manageSymbolsTab)
		self.symbolsList.pack(fill=tk.BOTH, expand=1)
		
		# plot symbols tab - symbols list
		self.plotFrame = tkplot.PlottingFrame(plotTab)
		self.plotFrame.pack(fill=tk.BOTH, expand=1)
		
		# button bar
		btnFrame = tk.Frame(manageSymbolsTab)
		btnFrame.pack(fill=tk.BOTH, expand=0)
		btnAdd = tk.Button(btnFrame, text="Add new", command=self.symbol_add)
		btnRefresh = tk.Button(btnFrame, text="Refresh selected", command=self.symbol_refreshEoD)
		btnAdd.pack(side=tk.RIGHT)
		btnRefresh.pack(side=tk.RIGHT)
		
		# FIXME: delete following rows
		self.source = yahoo.LocalSource(DEFAULT_DATABASE_PATH)
		self.symbolsList.refresh(self.source)
		self.plotFrame.refresh(self.source)
			

	def database_new(self):
		"""Create a new database file"""

		filename = tkFileDialog.asksaveasfilename()
		
		if filename:
			self.con.info("User asked to create a new database named {0}".format(filename))
			self.source = yahoo.LocalSource(filename)
		

	def database_open(self):
		"""Open an existing database"""
	
		filename = tkFileDialog.askopenfilename(multiple=False)

		if filename:
		
			try:
				self.con.info("Trying to load file {0}".format(filename))
				self.source = yahoo.LocalSource(filename)
			except Exception, ex:
				self.con.critical("Cannot open file {0} as local database".format(filename))
				self.con.error(ex.message)
			
			self.symbolsList.refresh(self.source)
			self.plotFrame.refresh(self.source)
	
	def symbol_load_from_file(self):
		"""Add a group of symbols starting from one CSV index file"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
			
		w = tksym.WindowAddFromFile(self.root, self.source)
		self.symbolsList.refresh(self.source)
		self.plotFrame.refresh(self.source)
			

	def symbol_add(self):
		"""Add new symbol to database"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
			
		w = tksym.WindowAdd(self.root, self.source)
		self.symbolsList.refresh(self.source)
		self.plotFrame.refresh(self.source)
		
			
	def symbol_refreshEoD(self):
	
		selectedIndexes = self.symbolsList.get_selected()
		
		for idx in selectedIndexes:
		
			symbol = self.symbolsList.get_item(idx)["text"]
			
			try:
				self.con.info("Refreshing symbol {0}".format(symbol))
				self.log.info("Refreshing symbol {0}".format(symbol))
				self.source.symbol_refresh_eod(symbol)
				
			except Exception, ex:
				self.log.error(traceback.format_exc())
				self.con.error("Cannot refresh symbol {0}".format(symbol))
				self.con.error(ex.message)
				continue
			
		self.symbolsList.refresh(self.source)
		self.plotFrame.refresh(self.source)

		
	def symbol_plot(self):
		
		pass
	
	def quit(self):
	
		self.root.quit()
		self.root.destroy()
	
		

if __name__ == '__main__':

	root = tk.Tk()
	app = Application(root)
	root.mainloop()
