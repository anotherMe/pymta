#!/usr/bin/python

import yahoo
from plotting import Plotter
import market
import argparse
import datetime
import logging

logging.basicConfig(filename='plotting_test.log', level=logging.DEBUG, format='%(asctime)s %(message)s') # log to file
log = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('source', help='path to the LocalSource database')
parser.add_argument('-s', '--symbol', required=True,
	help='the symbol to plot, according to yahoo convention (ie: SPM.MI)')
args = parser.parse_args()

datasource = yahoo.LocalSource(args.source)

mindate = '2015-03-01'
maxdate = '2016-03-01'
symbol = market.Symbol(datasource, args.symbol, mindate, maxdate, matplotlib=True)


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
