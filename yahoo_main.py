#!/usr/bin/python

"""Helper script used to automate basic operation on a yahoo.LocalSource
"""

import yahoo


if __name__=='__main__':

	source = yahoo.LocalSource("yahoo.db3")
	#~ source._load_index_from_csv("FTSEMIB.MI", "data/FTSEMIB.MI.csv", "FTSE MIB")
	#~ source._load_index_from_csv("^DJI", "data/DJIA.csv", "Dow Jones Industrial Average")
	#~ source.load_all()
	source.refresh_all()
