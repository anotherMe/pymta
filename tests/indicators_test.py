
import unittest
import indicators
import yahoo
import os
import random
import pdb
import market

TEST_DB3_FILE = "yahoo.db3"
TEST_SYMBOL = "SPM.MI"


def silentremove(filename):
	"""Remove given filename if exists. Fails silently.
	"""
	try:
		os.remove(filename)
	except OSError:
		pass


class SymbolAnalyzer_test(unittest.TestCase):

	def setUp(self):

		source = yahoo.LocalSource(TEST_DB3_FILE)
		self.symbol = market.Symbol(source, TEST_SYMBOL)
	
	def tearDown(self):
		pass
		

	@unittest.skip("TODO")
	def test_get_closings_wVolumes(self):
		pass

	def test_get_closings(self):
		rows = self.symbol.get_closings()
		self.assertTrue( len(rows) > 0 )

	@unittest.skip("TODO")
	def test_get_maxdate(self):
		pass

	@unittest.skip("TODO")
	def test_get_mindate(self):
		pass

	@unittest.skip("TODO")
	def test_get_movingaverage(self):
		pass

	@unittest.skip("TODO")
	def test_get_ochlv(self):
		pass
				
	def test_get_onbalancevolume(self):
		
		volumes = self.symbol.get_volumes()
		rows = self.symbol.get_onbalancevolume()
		self.assertTrue( len(rows) > 0 )

	@unittest.skip("TODO")
	def test_get_volumes(self):
		pass

	@unittest.skip("TODO")
	def test_set_maxdate(self):
		pass

	@unittest.skip("TODO")
	def test_set_mindate(self):
		pass
		
		

class StrategyMaCrossover_test(unittest.TestCase):

	def setUp(self):

		source = yahoo.LocalSource(TEST_DB3_FILE)
		self.symbol = market.Symbol(source, TEST_SYMBOL, mindate = None, maxdate = None, matplotlib=False)
	
	def tearDown(self):
		pass

	def test_get_data(self):
		"""Given two MA, returns a non empty list of points.			
		"""

		strategy = indicators.StrategyMaCrossover(self.symbol, 50, 20)
		rows = strategy.get_data()
		self.assertTrue(len(rows) > 0)



if __name__ == '__main__':
	
	unittest.main()
