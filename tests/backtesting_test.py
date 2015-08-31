
import unittest
import backtesting
import yahoo
import indicators


TEST_SYMBOL = "ENI.MI"

class Test_test(unittest.TestCase):
	
	def setUp(self):
		self.source = yahoo.LocalSource("yahoo.db3")
		
	def tearDown(self):
		pass

	def test_run(self):
		
		symbol = self.source.get_symbol(TEST_SYMBOL)
		strategy = indicators.StrategyMaCrossover(symbol, 200, 50)
		test = backtesting.Test(strategy, initial_investment=10000.00, transaction_cost=9.00, ongoing_charges=None)
		
		result = test.run()
		
		self.assertIsInstance(result, backtesting.Result)



if __name__ == '__main__':
	
	unittest.main()
