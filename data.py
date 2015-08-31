


class Source(object):
	"""Not to be instantiated explicitly. This class is just an interface
	all the data sources should adhere.
	"""
	def __init__(self):
		pass
		
	def query(self):
		raise Exception("Not implemented")
		
