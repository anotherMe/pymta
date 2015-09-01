
import yahoo
import unittest
import datetime
import sqlite3
import os
import market

import pdb


TEST_DB3_FILE = "tests/test.db3"
TEST_CSV = "tests/test.csv"
TEST_SYMBOL = "TEST"
ONLINE_TEST_SYMBOL = "ENI.MI" # for testing yahoo online database



def silentremove(filename):
	"""Remove given filename if exists. Fails silently.
	"""
	try:
		os.remove(filename)
	except OSError:
		pass


class OnlineSource(unittest.TestCase):
	
	def setUp(self):
		self.source = yahoo.OnlineSource()
		
	def tearDown(self):
		pass
		
	def test_parsedatestring(self):
		datetime_obj = datetime.datetime.strptime('1974-09-03', '%Y-%m-%d')
		unixtime = int(datetime_obj.strftime('%s'))
		self.assertEqual(self.source._parsedatestring('1974-09-03'), unixtime)
		
	def test_get_closings(self):
		rows = self.source._get_closings(ONLINE_TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 2)
		
	def test_get_volumes(self):
		rows = self.source._get_volumes(ONLINE_TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 2)
		
	def test_get_ochlv(self):
		rows = self.source._get_ochlv(ONLINE_TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 6)
		
	def test_exists(self):
		self.assertTrue(self.source.exists(ONLINE_TEST_SYMBOL))

	def test_exists_not(self):
		self.assertFalse(self.source.exists('YARGLA.MI'))

	def test_download2csv(self):
		fh = self.source.download2csv(ONLINE_TEST_SYMBOL)
		self.assertTrue(os.path.isfile(fh[0]))
		silentremove(fh[0])

	def test_get_maxdate(self):
		maxdate = self.source.get_maxdate(ONLINE_TEST_SYMBOL)
		self.assertIsInstance(maxdate, datetime.datetime)


class LocalSource(unittest.TestCase):

	def setUp(self):
		
		silentremove(TEST_DB3_FILE)
		self.source = yahoo.LocalSource(TEST_DB3_FILE)
		self.source._load_from_csv(TEST_SYMBOL, TEST_CSV) # load fake prices as symbol `TEST`
	
	def tearDown(self):
		
		self.source.close()
		silentremove(TEST_DB3_FILE)

	def test_delete(self):		
		
		self.source._delete(TEST_SYMBOL)
		
		conn = sqlite3.connect(TEST_DB3_FILE)
		cur = conn.cursor()
		cur.execute("select count(*) from DAT_EoD")
		rowcount = cur.fetchone()
		self.assertTrue(rowcount[0] == 0)
		conn.close()
		
	def test_load(self):
		
		conn = sqlite3.connect(TEST_DB3_FILE)
		cur = conn.cursor()
		cur.execute("select count(*) from DAT_EoD where symbol = '{0}'".format(TEST_SYMBOL))
		rowcount = cur.fetchone()
		self.assertTrue(rowcount[0] > 0)
		conn.close()

	def testquery_simple(self):
		data = self.source._query("TEST")
		self.assertTrue(len(data) > 0)

	def testquery_wColumns(self):
		data = self.source._query("TEST", columns=['date', 'volume', 'close'])
		self.assertTrue(len(data) > 0)

	def test_exists(self):
		self.assertTrue(self.source.exists(TEST_SYMBOL))
	
	def test_get_all_symbols(self):
		symbols = self.source._get_all_symbols()
		self.assertTrue( len(symbols) > 0 )
		
	def test_get_maxdate(self):
		
		maxdate = self.source.get_maxdate(TEST_SYMBOL)
		self.assertIsInstance(maxdate, datetime.datetime)

	def test_get_closings(self):
		rows = self.source._get_closings(TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 2)
		
	def test_get_volumes(self):
		rows = self.source._get_volumes(TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 2)
		
	def test_get_ochlv(self):
		rows = self.source._get_ochlv(TEST_SYMBOL)
		self.assertGreater(len(rows), 0)
		self.assertEqual(len(rows[0]), 6)

	@unittest.skip("Temporarily disabled because too expensive")
	def test_load_all(self):
		
		self.source._delete(TEST_SYMBOL)
		self.source.load_all()
		symbols = self.source._get_all_symbols()
		loaded_symbols = self.source._query("select symbol from DAT_EoD group by symbol")
		self.assertEqual(len(symbols), len(loaded_symbols))

	def test_load_from_csv(self):
		
		self.source._load_from_csv("LOADTEST", TEST_CSV)
		conn = sqlite3.connect(TEST_DB3_FILE)
		cur = conn.cursor()
		cur.execute("select count(*) from DAT_EoD where symbol = '{0}'".format("LOADTEST"))
		rowcount = cur.fetchone()
		conn.close()
		self.assertTrue(rowcount[0] > 0)
		

	@unittest.skip("ToDo")
	def test_refresh_all(self):
		pass	
	
	@unittest.skip("TODO :: proper way to test this method ?")
	def test_refresh(self):
		
		self.source.refresh(ONLINE_TEST_SYMBOL)
		
		conn = sqlite3.connect(TEST_DB3_FILE)
		cur = conn.cursor()		
		cur.execute("select date_STR from DAT_EoD where symbol = '{0}'"
			" order by date_STR desc limit 1".format(ONLINE_TEST_SYMBOL))

		maxdate_str = cur.fetchone()[0]
		conn.close()

		maxdate = datetime.datetime.strptime(str(maxdate_str), '%Y-%m-%d')
		today = datetime.datetime.today()
		delta = today - maxdate
		self.assertTrue(delta.days < 3) # 3 days, because of weekends
		
			
			

if __name__ == '__main__':
	
	unittest.main()
