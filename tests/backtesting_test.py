
import unittest
import backtesting

import yahoo
import indicators
import market


TEST_SYMBOL = "SPM.MI"

class Test_test(unittest.TestCase):
	
	def setUp(self):
		self.source = yahoo.LocalSource("yahoo.db3")
		
	def tearDown(self):
		pass

	def test_run(self):
		
		symbol = market.Symbol(self.source, TEST_SYMBOL, mindate = None, maxdate = None, matplotlib=False)
		strategy = indicators.StrategyMaCrossover(symbol, 50, 20)
		test = backtesting.Test(strategy, capital=10000.00, transaction_cost=9.00, ongoing_charges=None)
		
		result = test.run()
		
		self.assertIsInstance(result, backtesting.Result)



if __name__ == '__main__':
	
	unittest.main()
