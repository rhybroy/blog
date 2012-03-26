import requests
import re
import lemondb

if __name__ == "__main__":
    db = lemondb.connect("mysql", host="localhost", user="root", passwd="", db="blog", charset="utf8")
    db2 = lemondb.connect("sqlite", db='e:/sqlite/pyblog.db', charset="utf8")
    contents = db.query("select * from typecho_contents")
    if contents != None:
        for con in contents:
            cid = con.cid
            title = con.title
            slug = con.slug
            created = con.created
            modified = con.modified
            markdown = con.markdown
            html = con.html
            db2.execute("insert into typecho_contents(cid, title, slug, created, modified, markdown, html) values(%s, %s, %s, %s, %s, %s, %s)", cid, title, slug, created, modified, markdown, html)
    print "DONE"