#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
import ttk

import tklib.console as tkcon
import tklib.symbol as tksym

import yahoo

VERSION="0.0.2"

class Application():

	
	def __init__(self, root):
		
		self.root = root
		self.source = None
		
		self.root.title("pymta tkInterface {0}".format(VERSION))

		menubar = tk.Menu(self.root)

		# file menu
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="New", command=self.database_new)
		filemenu.add_command(label="Open", command=self.database_open)
		filemenu.add_command(label="Exit", command=self.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		# display the menu
		self.root.config(menu=menubar)
		
		# create the main frame
		self.mainFrame = tk.Frame(self.root)
		self.mainFrame.pack(fill=tk.BOTH, expand=1)
		
		# show console window
		self.con = tkcon.Window(self.root)
		
		self.createWidgets()
		
		# FIXME: delete following rows
		self.source = yahoo.LocalSource("/home/marco/lab/pymta/yahoo.db3")
		self.refreshSymbolsList()


	def createWidgets(self):
		
		listFrame = tk.Frame(self.mainFrame)
		listFrame.pack(fill=tk.BOTH, expand=1)
		
		scrollbar = tk.Scrollbar(listFrame)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.symbolsList = ttk.Treeview(listFrame, columns=["descr"])
		self.symbolsList.pack(fill=tk.BOTH, expand=1)
		
		self.symbolsList.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.symbolsList.yview)

		btnFrame = tk.Frame(self.mainFrame)
		btnFrame.pack(fill=tk.BOTH, expand=0)
		btnAdd = tk.Button(btnFrame, text="Add", command=self.symbol_add)
		btnLoad = tk.Button(btnFrame, text="Load from file", command=self.symbol_load_from_file)
		btnAdd.pack(side=tk.LEFT)
		btnLoad.pack(side=tk.LEFT)
		

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
			self.con.info("User asked to open file {0}".format(filename))
			self.source = yahoo.LocalSource(filename)
			self.refreshSymbolsList()
	
	def symbol_load_from_file(self):
		"""Add a group of symbols starting from one CSV index file"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
			
		w = tksym.WindowAddFromFile(self.root, self.source)
			

	def symbol_add(self):
		"""Add new symbol to database"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
		
	def refreshSymbolsList(self):
		
		symbols = self.source.symbol_get_all()
		for symbol in symbols:
			print symbol
			#~ self.symbolsList.insert('', 'end', text=symbol[0], values=("{0}".format(symbol[1].encode('ascii','replace'))))
			#~ self.symbolsList.insert('', 'end', text=symbol[0], values=[symbol[1].encode('ascii','replace')])
			self.symbolsList.insert('', 'end', text=symbol[0], values=[symbol[1]])
		
			
	def quit(self):
	
		self.root.quit()
		self.root.destroy()
		
		
		

if __name__ == '__main__':

	root = tk.Tk()
	app = Application(root)
	root.mainloop()
