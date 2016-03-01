
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox

import pdb

class SymbolList(tk.Frame):
	
	def __init__(self, master):
		
		tk.Frame.__init__(self, master)

		scrollbar = tk.Scrollbar(self)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.symbolsList = ttk.Treeview(self, columns=["descr", "last_updated"])
		self.symbolsList.pack(fill=tk.BOTH, expand=1)
		
		self.symbolsList.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.symbolsList.yview)
		
		# context menu
		# self.popup = tk.Menu(self.symbolsList, tearoff=0)
		# self.popup.add_command(label="Refresh EoD", command=self.symbol_refreshEoD)
		# self.popup.add_command(label="Plot", command=self.symbol_plot)
		# self.symbolsList.bind("<Button-3>", self.do_popup)
		
	def refresh(self, datasource):
		"""Rescan database to retrieve all the stored symbols"""
		
		items = self.symbolsList.get_children()
		if items != ():
			for item in items:
				self.symbolsList.delete(item)
			
		symbols = datasource.symbol_get_all()
		for symbol in symbols:
			self.symbolsList.insert('', 'end', text=symbol[0], values=[symbol[1], symbol[2]])
		
	# def do_popup(self, event):
		
		# try:
			# self.popup.tk_popup(event.x_root, event.y_root, 0)
		# finally:
			# self.popup.grab_release()
			
			

class WindowAdd(tk.Toplevel):
	
	def __init__(self, master):
		
		tk.Toplevel.__init__(self, master)
		
		mainFrame = tk.Frame(self)
		mainFrame.pack(fill=tk.BOTH, expand=1)


class WindowAddFromFile(tk.Toplevel):

	def __init__(self, parent, dataSource):

		tk.Toplevel.__init__(self, parent)
		
		self.source = dataSource
		
		self.transient(parent)
		self.title("Load symbols from file")
		self.parent = parent
		self.result = None

		body = tk.Frame(self)
		self.initial_focus = self
		body.pack()

		fileFrame = tk.Frame(body)
		fileFrame.pack(fill=tk.BOTH, expand=1, pady=5)
		fileLabel = tk.Label(fileFrame, text="Filename")
		fileLabel.pack(side=tk.LEFT)
		self.fileEntry = tk.Entry(fileFrame)
		self.fileEntry.pack(side=tk.LEFT, padx=5)
		fileBtn = tk.Button(fileFrame, text="File ...", command=self.chooseFile)
		fileBtn.pack(side=tk.LEFT, padx=5)
		
		nameFrame = tk.Frame(body)
		nameFrame.pack(fill=tk.BOTH, expand=1, pady=5)
		nameLabel = tk.Label(nameFrame, text="Index name")
		nameLabel.pack(side=tk.LEFT)
		self.nameEntry = tk.Entry(nameFrame)
		self.nameEntry.pack(side=tk.LEFT)
		
		descrFrame = tk.Frame(body)
		descrFrame.pack(fill=tk.BOTH, expand=1, pady=5)
		descrLabel = tk.Label(descrFrame, text="Index description")
		descrLabel.pack(side=tk.LEFT)
		self.descrEntry = tk.Entry(descrFrame)
		self.descrEntry.pack(side=tk.LEFT)
		
		btnBox = tk.Frame(body)
		w = tk.Button(btnBox, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(btnBox, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		btnBox.pack()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)


	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()
		self.apply()
		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		if self.fileEntry.get().strip() == '':
			tkMessageBox.showwarning("pymta", "File entry is empty")
			return 0
		
		if self.nameEntry.get().strip() == '':
			tkMessageBox.showwarning("pymta", "Name entry is empty")
			return 0
		
		#~ if self.descrEntry.get().strip() == '':
			#~ tkMessageBox.showwarning("pymta", "Description entry is empty")
			#~ return 0
		
		return 1 # override


	def apply(self):

		self.source.symbol_load_from_csv(self.fileEntry.get(), self.nameEntry.get(), self.descrEntry.get())
		

	def chooseFile(self):
		
		filename = tkFileDialog.askopenfilename(multiple=False)
		self.fileEntry.delete(0, tk.END)
		self.fileEntry.insert(0, filename)
		
		
