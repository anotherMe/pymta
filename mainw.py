#!/usr/bin/env python

import Tkinter as tk
import tkFileDialog
#~ import ttk

import tklib.console as tkcon
import tklib.symbol as tksym

import pdb

import yahoo


class Application():

	
	def __init__(self, root):
		
		self.root = root
		self.source = None
		
		# FIXME: only for dev
		self.source = yahoo.LocalSource("/home/marco/lab/pymta/yahoo.db3")
		
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
		
		# FIXME: only for dev
		self.symbol_load_from_file()

	def createWidgets(self):
		
		# symbols list box
		listBox = tk.Listbox(self.mainFrame)
		listBox.insert(tk.END, "No symbols loaded")
		listBox.pack(fill=tk.BOTH, expand=1)

		btnFrame = tk.Frame(self.mainFrame)
		btnFrame.pack(fill=tk.BOTH, expand=1)
		
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
	
	def symbol_load_from_file(self):
		"""Add a group of symbols starting from one CSV index file"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
			
		w = tksym.WindowAddFromFile(self.root)
			

	def symbol_add(self):
		"""Add new symbol to database"""
		
		if self.source == None:
			self.con.info("You need to open a database first")
			return
		
		
			
	def quit(self):
	
		self.root.quit()
		self.root.destroy()
		
		
		

if __name__ == '__main__':

	root = tk.Tk()
	app = Application(root)
	root.mainloop()
