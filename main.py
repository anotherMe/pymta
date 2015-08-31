#!/usr/bin/python

import yahoo
from plotting import Plotter
import indicators
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
	symbol = source.get_symbol(args.symbol)
	symbol.mindate = args.mindate
	symbol.maxdate = args.maxdate
	
	augmented = indicators.SymbolAnalyzer(symbol, True)
	
	p = Plotter()
	#~ p.draw_simple(augmented)
	#~ p.draw_candlestick(augmented)
	#~ p.draw_simple_with_volume(augmented)
	#~ p.draw_simple_with_volume_obv(augmented)
	#~ p.draw_moving_averages(augmented, [50, 20, 12])
	#~ ###p.draw([augmented], args.mindate, args.maxdate, [50,200], False)
	
	p.draw_moving_average_crossover(symbol, 50, 20)
	
	p.run()
	
