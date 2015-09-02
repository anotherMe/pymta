
import unittest
import market
import yahoo
import datetime
from matplotlib import dates as mdates
import os

import pdb

TEST_DB3_FILE = "tests/test.db3"
TEST_CSV = "tests/test.csv"
TEST_SYMBOL = "TEST"



def silentremove(filename):
	"""Remove given filename if exists. Fails silently.
	"""
	try:
		os.remove(filename)
	except OSError:
		pass
		

class Symbol(unittest.TestCase):
	
	def setUp(self):
		silentremove(TEST_DB3_FILE)
		self.source = yahoo.LocalSource(TEST_DB3_FILE)
		self.source._load_from_csv(TEST_SYMBOL, TEST_CSV) # load fake prices as symbol `TEST`
		self.symbol = market.Symbol(self.source, TEST_SYMBOL)
		
	def tearDown(self):	
		silentremove(TEST_DB3_FILE)

	def test_get_closings(self):
		data = self.symbol.get_closings()
		self.assertTrue(len(data) > 0)
		
	def test_get_movingaverage(self):
		data = self.symbol.get_movingaverage(40)
		self.assertTrue(len(data) > 0)
		
	def test_get_ochlv(self):
		data = self.symbol.get_ochlv()
		self.assertTrue(len(data) > 0)
		
	def test_get_onbalancevolume(self):
		data = self.symbol.get_onbalancevolume()
		self.assertTrue(len(data) > 0)
		
	def test_get_volumes(self):
		data = self.symbol.get_volumes()
		self.assertTrue(len(data) > 0)
		
	def test_transform_date(self):
		birthday_str = '1974-09-03'
		fmt = '%Y-%m-%d'
		birthday_unixtime = int(datetime.datetime.strptime(birthday_str, fmt).strftime("%s"))
		birthday_matplotlib = mdates.num2date(self.symbol.transform_date(birthday_unixtime))
		self.assertEqual(birthday_matplotlib.strftime(fmt), birthday_str)


if __name__ == '__main__':
	
	unittest.main()
