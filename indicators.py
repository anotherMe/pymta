
import logging as log
log.basicConfig(filename='indicators.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import matplotlib.pyplot as plt
import matplotlib
import numpy
import pdb

BUY = 1
SELL = -1


"""TODO: at the moment, every moment reloads data from the source, in 
order to filter on mindate and maxdate directly from the datasource.
Maybe it's more performing to load all the data on __init__ method and
filter on the in memory data every time a method is called.
"""


class SymbolAnalyzer:
	"""A decorator for the yahoo._Symbol class. Augmented symbols 
	instances, can be queried for technical analysis data.
	"""
	
	def __init__(self, symbol, matplotlib=False):
		
		self.symbol = symbol
		self.matplotlib_formatted_dates = matplotlib
	
	
	def get_data_DELETE(self, columns=[], mindate = None, maxdate = None):
		return self.symbol.get_data(columns, mindate, maxdate)
		
	
	def get_onbalancevolume(self):
		"""Retrieve a timeseries of closings with associated volumes:
		
			[(date1, closing1, volume1), (date2, closing2, volume2), ...]
		
		then returns a timeseries with the same dimension, containing the 
		OBVs:
			
			[(date1, obv1), (date2, obv2), ...]


		The OBV is calculated according to Joe Granville's original 
		version of the OBV: we add volume on days that the close is 
		higher than the day before and subtract the volume on days that 
		the price is lower than the day before.
		"""


		closings = self.get_closings()
		volumes = self.get_volumes()
		
		tclosings = numpy.transpose(closings)
		tvolumes = numpy.transpose(volumes)
		
		tdata = [tclosings[0], tclosings[1], tvolumes[1]]
		data = numpy.transpose(tdata)
		
		
		results = []
		for idx in range(len(data)):
		
			#~ print "Before {0}".format(obv)
			#~ print "Volume {0}".format(closings[idx][2])
			#~ print "Price diff {0}".format(closings[idx-1][1] - closings[idx][1])
			
			if idx == 0:
				obv = data[idx][2] # set starting volume
				
			# compare prices
			elif closings[idx-1][1] < data[idx][1]:
				obv += data[idx][2] # add volume
				
			else:
				obv -= data[idx][2] # subtract volume
				
			#~ print "After {0}".format(obv)
			#~ print ""
				
			results.append(tuple([data[idx][0], obv]))
				
		return results
	
	
	
	def get_volumes(self):
		"""Return a timeseries:
		
			[(date1, volume1), (date2, volume2), ...]
			
		"""
		
		data = self.symbol.get_data(['date_UNIX', 'volume'])

		for idx in range(len(data)):
			data[idx] = (self.transform_date(data[idx][0]), data[idx][1])

		return data
		
	
	def get_ochlv(self):
		"""Return an array of points:
		
			([(date1, open1, close1, high1, low1),
				(date1, open1, close1, high1, low1), ... ]
			
		"""
		
		data = self.symbol.get_data(['date_UNIX', 'open', 'close', 'high', 'low'])
		
		for idx in range(len(data)):
			data[idx] = (self.transform_date(data[idx][0]), # date
				data[idx][1], # open
				data[idx][2], # close
				data[idx][3], # high
				data[idx][4] # low
			)
		
		return data
		
	
	def get_closings(self):
		"""Return an array of points:
		
			[(date1, close1), (date2, close2), ...]
			
		"""
		
		data = self.symbol.get_data(['date_UNIX', 'close'])

		for idx in range(len(data)):
			data[idx] = (self.transform_date(data[idx][0]), data[idx][1])
		
		return data
		
		
	def get_movingaverage (self, window):

		closings = self.get_closings()
		tclosings = numpy.transpose(closings)

		weights = numpy.repeat(1.0, window)/window		
		sma = numpy.convolve(tclosings[1], weights, 'valid') # the MA is obtained using a convolution
		
		result = []
		for idx in range(len(sma)):
			result.append(tuple([tclosings[0][idx], sma[idx]]))
		
		return result
		

	def transform_date(self, mydate):
		"""All dates, in order to be processed by Matplotlib, must be
		transformed in float values.
		"""

		if self.matplotlib_formatted_dates:
			#~ return mdates.datestr2num(str(mydate))
			return matplotlib.dates.epoch2num(mydate)
		else:
			return mydate


class Strategy(object):
	"""A decorator for the yahoo._Symbol class. Strategy instances, can 
	be queried for technical analysis data with buy/sell indications.
	
	This is only a blue print for the other strategy classes.
	"""
	
	def __init__(self, symbol_analyzer, matplotlib):
		
		self.analyzer = symbol_analyzer
		self.matplotlib_formatted_dates = matplotlib

	def get_data(self):
		"""Returns a list of points with buy/sell indication:
		
			[(date1, value1, indication1), ... ]
			
		"""
		pass
		
	def transform_date(self, mydate):
		"""All dates, in order to be processed by Matplotlib, must be
		transformed in float values.
		"""

		if self.matplotlib_formatted_dates:
			#~ return mdates.datestr2num(str(mydate))
			return matplotlib.dates.epoch2num(mydate)
		else:
			return mydate
			
	

class StrategyMaCrossover(Strategy):
	"""Buy/Sell indications taken from crossover of two moving averages.
	"""
	
	def __init__(self, symbol_analyzer, period_slow, period_fast, matplotlib=False):
		"""
		Parameters:
			
			symbol :: a yahoo._Symbol instance
			period_slow :: period for the slowest moving average ( bigger period )
			period_fast :: period for the fast moving average ( smaller period )
			matplotlib :: select if returned timeseries should use matplotlib dates representation
			
		"""
		
		super(StrategyMaCrossover, self).__init__(symbol_analyzer, matplotlib)
		
		if period_slow <= period_fast:
			raise Exception("Slow period must be greater than fast period")
		
		self.slow = period_slow
		self.fast = period_fast
		

	def get_data(self):
		"""Given two timeseries (ie: two lists of points like these:
		
			[(date1, value1), (date2, value2), ...]
			
		returns a third timeseries containing only the points where the 
		two series overlap.
		
		Every overlapping point is marked with either:
		
			- BUY (1)
			- SELL(-1)
			
		The returned timeseries is something like:
		
			[(date1, value1, recommendation1), ...]
			
		"""
	
		maslow = self.analyzer.get_movingaverage(self.slow)
		mafast = self.analyzer.get_movingaverage(self.fast)
		
		# shift all points back by one ( repeat last point to maintain length )
		lastidx = len(maslow)-1
		previous_maslow = maslow[1:] + [maslow[lastidx]]
		lastidx = len(mafast)-1
		previous_mafast = mafast[1:] + [mafast[lastidx]]
		
		crossings = []
		for idx in range(len(maslow)): # maslow has more points than mafast
			crossing = 0
			if ((maslow[idx][1] <= mafast[idx][1]) & (previous_maslow[idx][1] >= previous_mafast[idx][1])):
				crossing = BUY
			if ((maslow[idx][1] >= mafast[idx][1]) & (previous_maslow[idx][1] <= previous_mafast[idx][1])):
				crossing = SELL
			crossings.append(tuple([maslow[idx][0], maslow[idx][1], crossing]))
		
		return crossings
		

		
