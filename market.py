
import logging as log
log.basicConfig(filename='market.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import numpy
from matplotlib import dates as mdates

		
class Symbol:
	"""This class provides all the methods used to retrieve data from
	a single stock.
	"""
	
	def __init__(self, datasource, symbol_name, mindate = None, maxdate = None, matplotlib=False):
		"""Parameters:
			
			datasource :: a valid data source
			symbol_name :: the symbol used to identify the stock; at the moment we use Yahoo convention ( ie: ENI.MI )
			mindate :: from date
			maxdate :: to date
			matplotlib :: say if we should use matplotlib date format 
			
		"""		
		self.name = symbol_name
		self.source = datasource
		self.matplotlib = matplotlib
		
		# just to save some typing, define mindate and maxdate as instance properties
		self.mindate = mindate
		self.maxdate = maxdate
		
	
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
		
		data = self.source.query(self.name, ['date', 'volume'], self.mindate, self.maxdate)

		for idx in range(len(data)):
			data[idx] = (self.transform_date(data[idx][0]), data[idx][1])

		return data
		
	
	def get_ochlv(self):
		"""Return an array of points:
		
			([(date1, open1, close1, high1, low1),
				(date1, open1, close1, high1, low1), ... ]
			
		"""
		
		data = self.source.query(self.name, ['date', 'open', 'close', 'high', 'low'], self.mindate, self.maxdate)
		
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
		
		data = self.source.query(self.name, ['date', 'close'], self.mindate, self.maxdate)

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

		if self.matplotlib:
			#~ return mdates.datestr2num(str(mydate))
			return mdates.epoch2num(mydate)
		else:
			return mydate
