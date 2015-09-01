#!/usr/bin/python

"""
	Launch all the plotting.Plotter class methods.
	
	This script is supposed to act as a test for the plotting.Plotter
	class.
	
"""

import yahoo
from plotting import Plotter
import market
import argparse

LOCAL_DATASOURCE = "yahoo.db3"
TEST_SYMBOL = "ENI.MI"


if __name__=='__main__':


	## plotting ##

	source = yahoo.LocalSource(LOCAL_DATASOURCE)
	symbol = market.Symbol(source, TEST_SYMBOL, None, None, matplotlib=True)
	
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
	
