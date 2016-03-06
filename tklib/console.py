
import Tkinter as tk

DEBUG="DEBUG"
INFO="INFO"
WARN="WARN"
ERROR="ERROR"
CRITICAL="CRITICAL"


class Frame(tk.Frame):
	
	def __init__(self, master):
		
		tk.Frame.__init__(self, master)

		scrollbar = tk.Scrollbar(self)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.console = tk.Text(self, yscrollcommand=scrollbar.set, bg="black", fg="green")
		self.console.config(state=tk.DISABLED)
		self.console.pack(fill=tk.BOTH, expand=1)
		
		self.console.tag_config(DEBUG, foreground="blue")
		self.console.tag_config(INFO, background="green", foreground="black")
		self.console.tag_config(WARN, foreground="yellow")
		self.console.tag_config(ERROR, foreground="red")
		self.console.tag_config(CRITICAL, background="yellow", foreground="red")

		scrollbar.config(command=self.console.yview)
			
	def debug(self, msg):
		
		self._log(DEBUG, msg)
		
	def info(self, msg):

		self._log(INFO, msg)

	def warn(self, msg):
		
		self._log(WARN, msg)
		
	def error(self, msg):
		
		self._log(ERROR, msg)	
		
	def critical(self, msg):
		
		self._log(CRITICAL, msg)

	def _log(self, level, msg):
		"""Log a message to the console widget"""
		
		self.console.config(state=tk.NORMAL)
		self.console.insert(tk.END, level, (level))
		self.console.insert(tk.END, " :: ")
		self.console.insert(tk.END, msg)
		self.console.insert(tk.END, "\n")
		self.console.config(state=tk.DISABLED)
		self.console.update_idletasks() # force flush of tkText widget
