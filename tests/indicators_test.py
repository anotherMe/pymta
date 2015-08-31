
import unittest
import indicators
import yahoo
import os
import random
import pdb

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
		symbol = source.get_symbol(TEST_SYMBOL)
		self.indicator = indicators.SymbolAnalyzer(symbol)
	
	def tearDown(self):
		pass
		

	@unittest.skip("TODO")
	def test_get_closings_wVolumes(self):
		pass

	def test_get_closings(self):
		rows = self.indicator.get_closings()
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
		
		volumes = self.indicator.get_volumes()
		rows = self.indicator.get_onbalancevolume()
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
		self.symbol = source.get_symbol(TEST_SYMBOL)
		#~ self.indicator = indicators.SymbolAnalyzer(symbol)
	
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
