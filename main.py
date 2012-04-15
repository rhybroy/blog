import os
import tornado
import logging
from time import time
from tornado import web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options
from tornado.httpserver import HTTPServer
import settings as setting_parm

define("debug", default=True, help="debug mode")
define("cookie_secret", default="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        help="key for HMAC")
define("check_interval", default=60*60,
        help="the interval of checking login status")


class Application(web.Application):
    def __init__(self):
        
        settings = dict(
            debug=options.debug,
			autoescape=None,
            xsrf_cookies=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=options.cookie_secret,
            login_url="/auth/login",
        )
        
        import sys
        sys.path.append("dbutil")
        import lemondb
        self.db = lemondb.connect(options.database, **setting_parm.database_types[options.database])
        
        from handlers import handlers
        super(Application, self).__init__(handlers, **settings)

def main():
    tornado.options.parse_command_line()

    http_server = HTTPServer(Application(), xheaders=True)
    http_server.bind(options.port)
    http_server.start()

    IOLoop.instance().start()

if __name__ == "__main__":
    main()

