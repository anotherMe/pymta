#!/usr/bin/python

import yahoo
from plotting import Plotter
import market
import argparse



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

	source = yahoo.LocalSource(LOCAL_DATASOURCE)
	symbol = market.Symbol(source, args.symbol, args.mindate, 
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
		
		
