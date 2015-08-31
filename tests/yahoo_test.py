
import yahoo

import unittest
import datetime
import sqlite3
import os


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



class _Symbol(unittest.TestCase):
	
	def setUp(self):
		silentremove(TEST_DB3_FILE)
		self.source = yahoo.LocalSource(TEST_DB3_FILE)
		self.source._load_from_csv(TEST_SYMBOL, TEST_CSV) # load fake EoDs as symbol `TEST`
		
	def tearDown(self):
		silentremove(TEST_DB3_FILE)
		
	def test_get_data(self):
		symbol = yahoo._Symbol(self.source, "TEST")
		data = symbol.get_data()
		self.assertTrue(len(data) > 0)



class OnlineSource(unittest.TestCase):
	
	def setUp(self):
		self.source = yahoo.OnlineSource()
		
	def tearDown(self):
		pass
		
	@unittest.skip("ToDo")
	def test_query_001(self):
		data = self.source._query(ONLINE_TEST_SYMBOL, '2010-01-01', '2011-01-01')
		self.assertTrue(len(data) > 0)

	@unittest.skip("ToDo")
	def test_query_002(self):
		data = symbol._query(ONLINE_TEST_SYMBOL, '2009-01-01', '2010-01-01')
		self.assertIsInstance(data[0], sqlite3.Row)
		
	def test_exists(self):
		self.assertTrue(self.source.exists(ONLINE_TEST_SYMBOL))

	def test_download2csv(self):
		fh = self.source.download2csv(ONLINE_TEST_SYMBOL)
		self.assertTrue(os.path.isfile(fh[0]))
		silentremove(fh[0])
	
	@unittest.skip("ToDo")	
	def test_get_symbol(self):
		symbol = self.source.get_symbol(ONLINE_TEST_SYMBOL)
		self.assertTrue(symbol.name == ONLINE_TEST_SYMBOL)

	@unittest.skip("ToDo")
	def test_get_maxdate(self):
		pass


class LocalSource(unittest.TestCase):

	def setUp(self):
		
		silentremove(TEST_DB3_FILE)
		self.source = yahoo.LocalSource(TEST_DB3_FILE)
		self.source._load_from_csv(TEST_SYMBOL, TEST_CSV) # load fake prices as symbol `TEST`

	
	def tearDown(self):
				
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

	def test_query_001(self):
		data = self.source._query("TEST")
		self.assertTrue(len(data) > 0)

	def test_query_002(self):
		data = self.source._query("TEST", columns=['date_UNIX', 'volume', 'close'])
		self.assertTrue(len(data) > 0)

	@unittest.skip("TODO")
	def test_initialize(self):
		pass	

	@unittest.skip("TODO")
	def test_exists(self):
		pass

	def test_get_symbol(self):
		symbol = self.source.get_symbol(TEST_SYMBOL)
		self.assertIsInstance(symbol, yahoo._Symbol)
	
	def test_get_all_symbols(self):
		symbols = self.source._get_all_symbols()
		self.assertTrue( len(symbols) > 0 )
		
		
	def test_get_maxdate(self):
		
		maxdate = self.source.get_maxdate(TEST_SYMBOL)
		self.assertIsInstance(maxdate, datetime.datetime)


	@unittest.skip("ToDo")
	def test_load_all(self):
		pass


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
		cur.execute("select date from DAT_EoD where symbol = '{0}'"
			" order by date desc limit 1".format(ONLINE_TEST_SYMBOL))

		maxdate_str = cur.fetchone()[0]
		conn.close()

		maxdate = datetime.datetime.strptime(str(maxdate_str), '%Y-%m-%d')
		today = datetime.datetime.today()
		delta = today - maxdate
		self.assertTrue(delta.days < 3) # 3 days, because of weekends
		
			
			

if __name__ == '__main__':
	
	unittest.main()
