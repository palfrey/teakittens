#!/usr/bin/env python
from wsgiref.handlers import CGIHandler
from wsgiref.util import request_uri
from codecs import getencoder
output_folder = "output"

try:
	exception = BaseException
except NameError: # python <2.5
	exception = Exception

import random
from cache import get_list
random.seed()

def get_html(tags):
	photos = get_list(count=150, tags=tags)
	photo = random.choice(photos.values())

	if photo["author"] == "":
		photo["author"] = "someone"

	encoder = getencoder("ascii")

	return encoder("<img style=\"max-height:300px; max-width: 450px; display:block;\" src=\"%s\" /><br />\n<small>By <a href=\"%s\">%s</a> on flickr"%(photo["image"], photo["page"], photo["author"]),"ignore")[0]

def teakittens(environ, start_response):
	from cStringIO import StringIO
	import traceback
	ret = StringIO()
	try:
		print >>ret, "<title>More tea and kittens</title>"
		print >>ret, """<h2>More tea and kittens</h2>
		Inspired by <a href="http://www.teaandkittens.co.uk/">Tea and Kittens</a>, plus
		the <a href="http://www.flickr.com/services/api/">Flickr API</a>. 
		<a href="http://github.com/palfrey/teakittens">Source code</a><br />
		"""
		print >>ret, "<table><tr><td>"
		print >>ret,get_html(tags=("teapot","tea","-sf","-friends","-seattle", "-cupcake", "-barbie"))
		print >>ret, "</td><td>"
		print >>ret,get_html(tags=("cats","cat","kitten", "-couple"))
		print >>ret, "</tr></table>"
		status = '200 OK'
		response_headers = [('Content-type','text/html')]
		start_response(status, response_headers)
		return [ret.getvalue()]

	except exception, e:
		status = '500 Exception'
		response_headers = [('Content-type','text/html')]
		start_response(status, response_headers)
		tr = traceback.format_exc()
		return ["%s<br />\n<pre>%s</pre>"%(ret.getvalue(),tr)]
	
if __name__ == "__main__":
	CGIHandler().run(teakittens)
