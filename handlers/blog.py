#!/usr/bin/env python

import tornado.web

import urllib
import markdown2
import time

from base import BaseHandler

class HomeHandler(BaseHandler):
	def get(self, page=1):
		keyword = self.get_argument("keyword", None);
		if keyword:
			self.redirect("/search/%s"%keyword)
			return
		pagesize = 2
		page = int(page)
		if page < 1:
			page = 1
		start = (page-1)*pagesize
		entries = self.db.query("SELECT a.*, c.name as category, c.slug as cslug FROM typecho_contents a, typecho_relationships b, typecho_metas c where a.status = 'publish' and a.cid = b.cid and b.mid = c.mid ORDER BY a.created "
								"DESC LIMIT %s, %s", start, pagesize)
		
		categorys = self.db.query("select * from typecho_metas where type='category' order by `order`")
		recentlys = self.db.query("select title, slug, created from typecho_contents order by created desc limit 10")
		
		self.render("index.html", entries=entries, nextpage=page+1, prepage=page-1, pagetype="page", categorys=categorys, recentlys=recentlys)


class EntryHandler(BaseHandler):
	def get(self, slug):
		if isinstance(slug, unicode):
			slug = slug.encode("utf8")
		slug = urllib.quote(slug).lower().strip()

		entry = self.db.get("SELECT * FROM typecho_contents WHERE slug = %s and status = 'publish'", slug)
		if not entry: 
			raise tornado.web.HTTPError(404)
		
		comments = self.db.query("select * from typecho_comments where cid = %s order by created", entry.cid)
		
		categorys = self.db.query("select * from typecho_metas where type='category' order by `order`")
		recentlys = self.db.query("select title, slug, created from typecho_contents order by created desc limit 10")
		
		self.render("entry.html", entry=entry, comments=comments, categorys=categorys, recentlys=recentlys)


class CategoryHandler(BaseHandler):
	def get(self, slug, page=1):
		if isinstance(slug, unicode):
			slug = slug.encode("utf8")
		slug = urllib.quote(slug).lower().strip()
		mid = self.db.get("select mid from typecho_metas where slug = %s", slug).mid
		pagesize = 2
		page = int(page)
		if page < 1:
			page = 1
		start = (page-1)*pagesize
		entries = self.db.query("SELECT a.*, c.name as category, c.slug as cslug FROM typecho_contents a, typecho_relationships b, typecho_metas c where a.cid = b.cid and b.mid = c.mid and b.mid = %s and a.status = 'publish' ORDER BY created DESC LIMIT %s, %s", mid, start, pagesize)
		
		categorys = self.db.query("select * from typecho_metas where type='category' order by `order`")
		recentlys = self.db.query("select title, slug, created from typecho_contents order by created desc limit 10")
		
		self.render("index.html", entries=entries, nextpage=page+1, prepage=page-1, pagetype="category/%s"%slug, categorys=categorys, recentlys=recentlys)

class SearchHandler(BaseHandler):
	def get(self, keyword, page=1):
		pagesize = 2
		page = int(page)
		if page < 1:
			page = 1
		start = (page-1)*pagesize
		entries = self.db.query("SELECT a.*, c.name as category, c.slug as cslug FROM typecho_contents a, typecho_relationships b, typecho_metas c where a.cid = b.cid and b.mid = c.mid and a.title like %s ORDER BY a.created DESC LIMIT %s, %s", "%"+keyword+"%", start, pagesize)
		
		categorys = self.db.query("select * from typecho_metas where type='category' order by `order`")
		recentlys = self.db.query("select title, slug, created from typecho_contents order by created desc limit 10")
		
		self.render("index.html", entries=entries, nextpage=page+1, prepage=page-1, pagetype="search/%s"%keyword, categorys=categorys, recentlys=recentlys)

class FeedHandler(BaseHandler):
	def get(self):
		entries = self.db.query("SELECT * FROM entries ORDER BY published "
								"DESC LIMIT 10")
		self.set_header("Content-Type", "application/atom+xml")
		self.render("feed.xml", entries=entries)



class EntryModule(tornado.web.UIModule):
	def render(self, entry):
		return self.render_string("modules/entry.html", entry=entry)


handlers = [
			(r"/", HomeHandler),
			(r"/page/(\d+)/?", HomeHandler),
			(r"/category/([^/]+)/?", CategoryHandler),
			(r"/category/([^/]+)/(\d+)?/?", CategoryHandler),
			(r"/search/([^/]+)/?", SearchHandler),
			(r"/search/([^/]+)/(\d+)?/?", SearchHandler),
			(r"/entry/([^/]+)", EntryHandler),
			(r"/feed", FeedHandler),
		]