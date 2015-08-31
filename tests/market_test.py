
import unittest
import market
import yahoo
import datetime


TEST_DB3_FILE = "tests/test.db3"
TEST_CSV = "tests/test.csv"
TEST_SYMBOL = "TEST"


class Symbol(unittest.TestCase):
	
	def setUp(self):
		self.source = yahoo.LocalSource(TEST_DB3_FILE)
		self.source._load_from_csv(TEST_SYMBOL, TEST_CSV) # load fake prices as symbol `TEST`
		self.symbol = market.Symbol(self.source, TEST_SYMBOL)
		
	def tearDown(self):
		pass

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
		today_unix = int(datetime.datetime.now().strftime("%s"))
		tdata1 = self.symbol.transform_date(today_unix)
		self.symbol.matplotlib = True
		tdata2 = self.symbol.transform_date(today_unix)
		
		self.assertNotEqual(tdata2, tdata1)


if __name__ == '__main__':
	
	unittest.main()
