#!/usr/bin/env python

from lemondb import LemonDB, Row
import sqlite3
import time
import datetime

def _getobj(**args):
	return Sqlitedb(**args)

class Sqlitedb(LemonDB):
	def _connect(self):
		self._database = self._db_args["db"]
		sqlite3.register_converter('DATE', adapt_converter)
		self._conn = sqlite3.connect(self._database,detect_types=sqlite3.PARSE_DECLTYPES)
		self._conn.isolation_level=None
		#self._conn.row_factory = dict_factory
		self._cursor = self._conn.cursor()
		
	def reconnect(self):
		"""Closes the existing database connection and re-opens it."""
		self.close()
		self._connect()

	def _get(self, sql, *args):
		self._cursor.execute(sql)
		return self._cursor.fetchone()
	
	def _execute(self, cursor, query, parameters):
		query = query.replace('%s','?')
		try:
			return cursor.execute(query, parameters)
		except RuntimeError:
			logging.error("Error connecting to SQLITE on %s", self.host)
			self.close()
			raise
		
def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return Row(d)
	
def adapt_converter(datestr):
	if datestr:
		now = time.strptime(datestr, "%Y-%m-%d %X")
		return datetime.datetime( *now[:6] )

if __name__ == '__main__':
	sqlite = Sqlitedb(db='e:/sqlite/pyblog.db')
	row = sqlite.query("select created from typecho_contents limit 5")
	print row