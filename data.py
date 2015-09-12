
	
URL_CSV_DOWNLOAD = "http://real-chart.finance.yahoo.com/table.csv"


class Source(object):
	"""Not to be instantiated explicitly. This class is just an interface
	all the data sources should adhere.
	"""

	def __init__(self):
		pass
		
	def _get_closings(self):
		raise Exception("Not implemented yet")

	def _get_volumes(self):
		raise Exception("Not implemented yet")

	def _get_ochlv(self):
		raise Exception("Not implemented yet")
		
	def _get_url(self, symbol_name, mindate=None, maxdate=None, historical=True):
		"""Build the URL needed to download data from Yahoo Finance 
		site.
		
		Parameter:
		
			symbol_name: symbol name, according to Yahoo convention (ie: SPM.MI)
			mindate: string representing date in the format '%Y-%m-%d'
			maxdate: string representing date in the format '%Y-%m-%d'
			historical: query Yahoo historical data ( at the moment we know about this only type of data)
		"""
		
		url = URL_CSV_DOWNLOAD + "?s={0}".format(symbol_name)
		
		if mindate != None:
			url += "&a={0}&b={1}&c={2}".format(mindate.month - 1, mindate.day, mindate.year)
			
		if maxdate != None:
			url += "&d={0}&e={1}&f={2}".format(maxdate.month - 1, maxdate.day, maxdate.year)
			
		url += "&g=d" # daily data
		url += "&ignore=.csv"

		return url
