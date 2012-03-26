from tornado.options import define

mysql_settings = dict(
            host="localhost",
            user="root",
            passwd="",
            db="blog",
            charset="utf8",
)

sqlite_settings = dict(
            db="db/pyblog.db",
)

database_types = dict(
            mysql=mysql_settings,
            sqlite=sqlite_settings
)

define("port", default=8888, help="run on the given port", type=int)

define("database", default="sqlite", help="sqlite database path")


print 'import settings.py'