
import logging as log
log.basicConfig(filename='indicators.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import matplotlib.pyplot as plt
import matplotlib
import numpy
import pdb

BUY = 1
SELL = -1

class Strategy(object):
	"""Strategy instances, can be queried for technical analysis data 
	with buy/sell indications.
	
	This is only a blue print for the other strategy classes.
	"""
	
	def __init__(self, symbol_analyzer, matplotlib):
		
		self.analyzer = symbol_analyzer
		self.matplotlib_formatted_dates = matplotlib

	def get_data(self):
		"""Returns a list of points with buy/sell indication:
		
			[(date1, value1, indication1), ... ]
			
		"""
		raise Exception("Not implemented")
		
		
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
				crossings.append(tuple([maslow[idx][0], maslow[idx][1], BUY]))
			elif ((maslow[idx][1] >= mafast[idx][1]) & (previous_maslow[idx][1] <= previous_mafast[idx][1])):
				crossings.append(tuple([maslow[idx][0], maslow[idx][1], SELL]))
			else:
				pass # skip 
		
		return crossings
		

		
