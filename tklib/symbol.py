
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import yahoo

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
		
		
