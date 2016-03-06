
import matplotlib.pyplot as plt
import matplotlib.finance as fin
from matplotlib import dates as mdates
import numpy
import logging

import indicators


class Plotter:
	
	def __init__(self, title='No title'):
		self.title = title
	
	def draw_simple(self, symbol):
		
		data = symbol.get_closings()
		tdata = numpy.transpose(data)
		plt.plot_date(tdata[0], tdata[1], fmt="-")


	def draw_candlestick(self, symbol):
		"""NOTE: Too much points in the timeseries may produce a blank 
		plot.
		"""
		
		data = symbol.get_ochlv()
		
		ax = plt.subplot(111)
		fin.candlestick_ochl(ax, data, width=0.5, colorup=u'g', colordown=u'r', alpha=1.0)
		ax.xaxis_date()
		ax.autoscale_view()


	def draw_moving_average_crossover(self, symbol, period_slow, period_fast):
		
		strategy = indicators.StrategyMaCrossover(symbol, period_slow, period_fast, True)
		
		ax1 = plt.subplot(111)
		
		### plot closing values ###
		
		#~ closings = augmented.get_closings()		
		#~ tclosings = numpy.transpose(closings)
		#~ ax1.plot_date(tclosings[0], tclosings[1], fmt="-")
		
		### plot first moving average ###
		
		ma1 = symbol.get_movingaverage(period_slow)
		tma1 = numpy.transpose(ma1)
		ax1.plot_date(tma1[0], tma1[1], fmt="-")

		### plot second moving average ###
		
		ma2 = symbol.get_movingaverage(period_fast)
		tma2 = numpy.transpose(ma2)
		ax1.plot_date(tma2[0], tma2[1], fmt="-")
		
		### BUY / SELL points ###
		
		data = strategy.get_data()
		for idx in range(len(data)):
			if data[idx][2] == indicators.BUY:
				ax1.plot_date(data[idx][0], data[idx][1], fmt="go")
			elif data[idx][2] == indicators.SELL:
				ax1.plot_date(data[idx][0], data[idx][1], fmt="ro")
			else:
				pass
				
		ax1.autoscale_view()
	
	
	def draw_MODIFY(self, symbols_names, avgs=[], showVolume=False):

		subplots_num = len(symbols_names)*2 if showVolume==True else len(symbols_names)
		
		figure, axArr = plt.subplots(subplots_num, sharex=True)
		
		subplot_idx = 0
		for symbol_name in symbols_names:
			
			symbol = Symbol(self.src, symbol_name, mindate, maxdate)
			values = symbol.get_closings()
			tvalues = numpy.transpose(values)

			axArr[subplot_idx].plot_date(tvalues[0], tvalues[1], fmt="-")
			
			for avg_idx in range(0, len(avgs)):
				
				ma = symbol.get_movingaverage(avgs[avg_idx])
				axArr[subplot_idx].plot_date(ma[0], ma[1], fmt="-")
				
				# if this is not the first loop ...
				if avg_idx > 0:
					
					# compare the current MA with the previous one
					previous_ma = symbol.get_movingaverage(avgs[avg_idx-1])
					crossover = indicators.crossover(previous_ma, ma)
					
					xbuy = [elem for elem in crossover if elem[2] > 0] 
					xsell = [elem for elem in crossover if elem[2] < 0] 
					
					txbuy = numpy.transpose(xbuy)
					txsell = numpy.transpose(xsell)
					
					axArr[subplot_idx].plot_date(txbuy[0], txbuy[1], fmt="go")
					axArr[subplot_idx].plot_date(txsell[0], txsell[1], fmt="ro")
				
			
			axArr[subplot_idx].set_title('{0} day closing values'.format(symbol_name))

			if showVolume:
				
				subplot_idx += 1
				
				volumes = self.src.get_volumes(sym)
				tvolumes = numpy.transpose(volumes)
				
				axArr[subplot_idx].plot_date(tvolumes[0], tvolumes[1], fmt="-")
				
			subplot_idx += 1
			
	
	def draw_moving_averages(self, sample, avgs=[]):
		
		values = sample.get_closings()
		volumes = sample.get_volumes()
		
		tvalues = numpy.transpose(values)
		tvolumes = numpy.transpose(volumes)
		
		plt.subplot(211)
		plt.plot_date(tvalues[0], tvalues[1], fmt="-")
		
		for avg in avgs:
			ma = sample.get_movingaverage(avg)
			tma = numpy.transpose(ma)
			plt.plot_date(tma[0], tma[1], fmt="-")
		
		plt.title('{0} day closing values'.format(self.title))
		
		plt.subplot(212)
		plt.plot_date(tvolumes[0], tvolumes[1], fmt="-")
		
	
	def draw_simple_with_volume(self, sample):
		
		values = sample.get_closings()
		values = numpy.transpose(values)
		
		volumes = sample.get_volumes()
		volumes = numpy.transpose(volumes)
		
		plt.subplot(211)
		plt.plot_date(values[0], values[1], fmt="-")
		plt.title('{0} day closing values'.format(self.title))
		
		plt.subplot(212)
		plt.plot_date(volumes[0], volumes[1], fmt="-")


	def draw_simple_with_volume_obv(self, sample):
		
		## gather data ##
		
		values = sample.get_closings()
		volumes = sample.get_volumes()
		obvs = sample.get_onbalancevolume()
		
		## transpose timeseries before plotting ##
		
		values = numpy.transpose(values)
		volumes = numpy.transpose(volumes)
		obvs = numpy.transpose(obvs)
		
		## plotting ##
		
		plt.subplot(311)
		plt.plot_date(values[0], values[1], fmt="-")
		plt.title('{0} day closing values'.format(self.title))
		
		plt.subplot(312)
		plt.plot_date(volumes[0], volumes[1], fmt="-")
		
		plt.subplot(313)
		plt.plot_date(obvs[0], obvs[1], fmt="-")

		
	def run(self):
		
		# maximize window
		#~ mng = plt.get_current_fig_manager()
		#~ mng.resize(*mng.window.maxsize())
		
		plt.show()


if __name__=='__main__':

	## argument parsing ##

	parser = argparse.ArgumentParser()
	parser.add_argument('source', help='path to the LocalSource database')
	parser.add_argument('-s', '--symbol', required=True,
		help='the symbol to plot, according to yahoo convention (ie: SPM.MI)')
	parser.add_argument('-t', '--type', help='Type of plot requested.',
		choices=['simple', 'candle', 'volume', 'obv', 'ma', 'mac'],
		default='simple'
	)
	parser.add_argument('--mindate', help='(optional) plot from date')
	parser.add_argument('--maxdate', help='(optional) plot until date')
	args = parser.parse_args()
	

	## plotting ##

	datasource = yahoo.LocalSource(args.source)
	symbol = market.Symbol(datasource, args.symbol, args.mindate, 
		args.maxdate, matplotlib=True)
		
	if args.type == 'candle':
		p = Plotter('Candlestick')
		p.draw_candlestick(symbol)
		p.run()
		
	elif args.type == 'volume':
		p = Plotter('Simple with volume')
		p.draw_simple_with_volume(symbol)
		p.run()
		
	elif args.type == 'obv':
		p = Plotter('Simple with volume and OBV')
		p.draw_simple_with_volume_obv(symbol)
		p.run()
		
	elif args.type == 'ma':
		p = Plotter('Moving averages')
		p.draw_moving_averages(symbol, [50, 20, 12])
		p.run()
		
	elif args.type == 'mac':
		p = Plotter('Moving averages crossover')
		p.draw_moving_average_crossover(symbol, 50, 20)
		p.run()
	else:
		p = Plotter('Simple')
		p.draw_simple(symbol)
		p.run()
		
		
class Symbol:
	"""This class provides all the methods used to retrieve data from
	a single stock, applying all the necessary transformations in order
	to make the data processable from plotting library.
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
		
		data = self.source.symbol_get_volumes(self.name, self.mindate, self.maxdate)


		if self.matplotlib:
			for idx in range(len(data)):
				data[idx] = (self.transform_date(data[idx][0]), data[idx][1])

		return data
		
	
	def get_ochlv(self):
		"""Return an array of points:
		
			([(date1, open1, close1, high1, low1),
				(date1, open1, close1, high1, low1), ... ]
			
		"""
		
		data = self.source.symbol_get_ochlv(self.name, self.mindate, self.maxdate)
		
		if self.matplotlib:
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
		
		data = self.source.symbol_get_closings(self.name, self.mindate, self.maxdate)

		if self.matplotlib:
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
		

	def transform_date(self, inputdate):
		"""Parameters:
		
			inputdate: Unix time - int representing number of seconds from Epoch
			
		Returns date in matplotlib date format, that is float number of days since 0001
		"""

		return mdates.epoch2num(inputdate)

