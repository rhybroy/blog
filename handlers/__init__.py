# -*- encoding: utf-8 -*-

handlers = []

from handlers import blog, admin 

handlers.extend(blog.handlers)
handlers.extend(admin.handlers)
