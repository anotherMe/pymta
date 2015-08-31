
import matplotlib.pyplot as plt
import matplotlib.finance as fin
import numpy
import indicators
import indicators


import pdb

class Plotter:
	
	def __init__(self):
		pass
	
	def draw_simple(self, symbol):
		
		data = symbol.get_closings()
		data = numpy.transpose(data)
		plt.plot_date(data[0], data[1], fmt="-")


	def draw_candlestick(self, symbol):
		
		data = symbol.get_ochlv()
		#pdb.set_trace()
		#~ data = numpy.transpose(data)
		
		ax = plt.subplot(111)
		fin.candlestick_ochl(ax, data, width=0.5, colorup=u'g', colordown=u'r', alpha=1.0)
		ax.xaxis_date()
		ax.autoscale_view()


	def draw_moving_average_crossover(self, symbol, period_slow, period_fast):
		
		augmented = indicators.SymbolAnalyzer(symbol, True)
		strategy = indicators.StrategyMaCrossover(augmented, period_slow, period_fast, True)
		
		ax1 = plt.subplot(111)

		
		### plot closing values ###
		
		#~ closings = augmented.get_closings()		
		#~ tclosings = numpy.transpose(closings)
		#~ ax1.plot_date(tclosings[0], tclosings[1], fmt="-")
		
		### plot first moving average ###
		
		ma1 = augmented.get_movingaverage(period_slow)
		tma1 = numpy.transpose(ma1)
		ax1.plot_date(tma1[0], tma1[1], fmt="-")

		### plot second moving average ###
		
		ma2 = augmented.get_movingaverage(period_fast)
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
		
		plt.title('{0} day closing values'.format(sample.symbol.name))
		
		plt.subplot(212)
		plt.plot_date(tvolumes[0], tvolumes[1], fmt="-")
		
	
	def draw_simple_with_volume(self, sample):
		
		values = sample.get_closings()
		values = numpy.transpose(values)
		
		volumes = sample.get_volumes()
		volumes = numpy.transpose(volumes)
		
		plt.subplot(211)
		plt.plot_date(values[0], values[1], fmt="-")
		plt.title('{0} day closing values'.format(sample.symbol.name))
		
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
		plt.title('{0} day closing values'.format(sample.symbol.name))
		
		plt.subplot(312)
		plt.plot_date(volumes[0], volumes[1], fmt="-")
		
		plt.subplot(313)
		plt.plot_date(obvs[0], obvs[1], fmt="-")

		
	def run(self):
		
		# maximize window
		#~ mng = plt.get_current_fig_manager()
		#~ mng.resize(*mng.window.maxsize())
		
		plt.show()
