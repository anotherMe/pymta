#!/usr/bin/python

import yahoo
from plotting import Plotter
import market
import argparse

SQLITE_DATABASE = "yahoo.db3"


if __name__=='__main__':


	## argument parsing ##

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--symbol', required=True,
		help='the symbol to plot, according to yahoo convention (ie: SPM.MI)')
	parser.add_argument('--mindate', help='(optional) plot from date')
	parser.add_argument('--maxdate', help='(optional) plot until date')
	args = parser.parse_args()
	

	## plotting ##

	source = yahoo.LocalSource(SQLITE_DATABASE)
	symbol = market.Symbol(source, args.symbol, args.mindate, 
		args.maxdate, matplotlib=True)
	
	p = Plotter('Simple')
	p.draw_simple(symbol)
	p.run()
	
	p = Plotter('Candlestick')
	p.draw_candlestick(symbol)
	p.run()
	
	p = Plotter('Simple with volume')
	p.draw_simple_with_volume(symbol)
	p.run()
	
	p = Plotter('Simple with volume and OBV')
	p.draw_simple_with_volume_obv(symbol)
	p.run()
	
	p = Plotter('Moving averages')
	p.draw_moving_averages(symbol, [50, 20, 12])
	p.run()
	
	p = Plotter('Moving averages crossover')
	p.draw_moving_average_crossover(symbol, 50, 20)
	p.run()
	
