
import Tkinter as tk

class Window(tk.Toplevel):
	
	def __init__(self, master):
		
		tk.Toplevel.__init__(self, master)
		
		mainFrame = tk.Frame(self)
		mainFrame.pack(fill=tk.BOTH, expand=1)

		scrollbar = tk.Scrollbar(mainFrame)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.console = tk.Text(mainFrame, yscrollcommand=scrollbar.set, bg="black", fg="green")
		self.console.config(state=tk.DISABLED)
		self.console.pack(fill=tk.BOTH, expand=1)
		
		scrollbar.config(command=self.console.yview)
			

	def info(self, msg):
	
		self._log("INFO", msg)
		
	def error(self, msg):
		
		self._log("ERROR", msg)
	
	def debug(self, msg):
		
		self._log("DEBUG", msg)
	
	def warn(self, msg):
		
		self._log("WARN", msg)

	def _log(self, level, msg):
		"""Log a message to the console widget"""
		
		self.console.config(state=tk.NORMAL)
		self.console.insert(tk.END, msg)
		self.console.insert(tk.END, "\n")
		self.console.config(state=tk.DISABLED)
