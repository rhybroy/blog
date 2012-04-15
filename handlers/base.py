# -*- encoding: utf-8 -*-
# author: binux<17175297.hk@gmail.com>

import time
from tornado.web import RequestHandler
from session import session

class BaseHandler(RequestHandler):
    _start_time = time.time()
    _finish_time = None

    def request_time(self):
        """Returns the amount of time it took for this request to execute."""
        if self._finish_time is None:
            return time.time() - self._start_time
        else:
            return self._finish_time - self._start_time
    

    @property
    def db(self):
        return self.application.db

    @session
    def get_current_user(self):
        user_id = self.session.get("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM typecho_users WHERE name = %s", str(user_id))