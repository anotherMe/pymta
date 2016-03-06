
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
import plotting

import pdb


class PlottingFrame(tk.Frame):
	
	def __init__(self, master):
		
		tk.Frame.__init__(self, master)

		panedWindow = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
		panedWindow.pack(fill=tk.BOTH, expand=1)
		
		leftFrame = tk.Frame(panedWindow)
		#~ leftFrame.pack(fill=tk.BOTH, expand=1)
		
		scrollbar = tk.Scrollbar(leftFrame)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.symbolsList = ttk.Treeview(leftFrame, columns=["descr", "last_updated"], selectmode='browse')
		self.symbolsList.pack(fill=tk.BOTH, expand=1)
		
		self.symbolsList.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.symbolsList.yview)
		
		panedWindow.add(leftFrame)
		
		rightFrame = tk.Frame(panedWindow)
		#~ rightFrame.pack(fill=tk.BOTH, expand=1)
		btnPlot = tk.Button(rightFrame, text="Plot selected", command=self.plot)
		btnPlot.pack(fill=tk.BOTH, expand=1)
		
		panedWindow.add(rightFrame)
		
		# context menu
		# self.popup = tk.Menu(self.symbolsList, tearoff=0)
		# self.popup.add_command(label="Refresh EoD", command=self.symbol_refreshEoD)
		# self.popup.add_command(label="Plot", command=self.symbol_plot)
		# self.symbolsList.bind("<Button-3>", self.do_popup)
		
		
	def refresh(self, datasource):
		"""Rescan database to retrieve all symbols with some EoD data"""
		
		items = self.symbolsList.get_children()
		if items != ():
			for item in items:
				self.symbolsList.delete(item)
			
		symbols = datasource.symbol_get_all_loaded()
		for symbol in symbols:
			self.symbolsList.insert('', 'end', text=symbol[0], values=[symbol[1], symbol[2]])


	def plot(self):
		
		sel = self.symbolsList.selection()
		item = self.symbolsList.item(sel[0])
		symbol = item.get('text')
		pdb.set_trace()
		
		
	# def do_popup(self, event):
		
		# try:
			# self.popup.tk_popup(event.x_root, event.y_root, 0)
		# finally:
			# self.popup.grab_release()
