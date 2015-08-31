#!/usr/bin/env python2

import logging as log
log.basicConfig(filename='backtesting.log', level=log.DEBUG) # log to file
#~ log.getLogger().addHandler(log.StreamHandler()) # log to stderr too

import sqlite3
import pdb
import indicators
import math


class Trade:
	"""A single buy/sell operation."""
	
	def __init__(self, datetime, quantity, price, sign):
		"""Parameters:
			datetime :: timestamp of transaction
			quantity :: number of stocks traded
			price :: price paid for every instrument ( equity, ETF, ... )
			sign :: either indicators.BUY or indicators.SELL
		"""
		self.datetime = datetime
		self.quantity = quantity
		self.price = price
		self.sign = sign
		

class Result:
	"""Set of data, returned by every Test.run()"""
	
	def __init__(self, money, trades):
		"""Parameters:
		
			- money :: the amount of money at the end of the Test
			- trades :: a list of Trade objects
		"""
		pass
		
	
class Test:
	"""A single unit of test."""
	
	def __init__(self, strategy, capital=10000.00, transaction_cost=9.00, ongoing_charges=None):
		"""Parameters:
		
			strategy :: an indicators.Strategy object
			initial_investment :: initial amount of money invested
			transaction_cost :: per transaction costs
			ongoing_charges :: ongoing charges if applied ( like in the case of funds or ETF )
		"""
		
		self.strategy = strategy
		self.portfolio = int(0)
		self.capital = capital
		self.tcost = transaction_cost
		self.charges = ongoing_charges
		self.trade_history = []
		
	def run(self):

		result = Result(5000, [])
		data = self.strategy.get_data()

		for point in data:
			
			date = point[0]
			advice = point[2]
			unitprice = point[1]
			if advice == indicators.BUY:
				
				quantity = int(math.modf(self.capital / unitprice)[1]) # buy as much stocks as your whole capital permits
				self.portfolio += quantity
				totalcost = quantity * unitprice
				self.capital -= totalcost
				
				trade = Trade(date, quantity, unitprice, indicators.BUY)
				self.trade_history.append(trade)
				log.debug("{0} - Bought {1} for {2}, totalling {3}".format(date, quantity, unitprice, totalcost))
				
			elif advice == indicators.SELL:
				
				quantity = self.portfolio # sell all stocks
				self.portfolio = 0
				totalcost = quantity * unitprice
				self.capital += totalcost
				
				trade = Trade(date, quantity, unitprice, indicators.SELL)
				self.trade_history.append(trade)
				log.debug("{0} - :: Sold {1} for {2}, totalling {3}".format(date, quantity, unitprice, totalcost))
				
			else:
				pass
				
			
				
		return result
	
	

class Battery:
	"""A battery of tests. Test are added to a Battery and then run.
	"""
	
	def __init__(self):
		self.testlist = []

	def add_test(self, test):
		self.testlist.append(test)

