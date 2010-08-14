#!/usr/bin/env python
from wsgiref.handlers import CGIHandler
from wsgiref.util import request_uri
from codecs import getencoder
output_folder = "output"

try:
	exception = BaseException
except NameError: # python <2.5
	exception = Exception

import flickrapi
import random

(api_key, secret) = [x.strip() for x in file("secrets").readlines()]

flickr = flickrapi.FlickrAPI(api_key)

def rand_photo(tag):
	items = list(tag.find("photos"))
	return random.choice(items)

def get_html(tag, cluster_id):
	cluster = flickr.tags_getClusterPhotos(tag=tag, cluster_id=cluster_id)
	r = rand_photo(cluster)
	id = r.get("id")
	sizes = flickr.photos_getSizes(photo_id=id)
	for size in list(sizes.find("sizes")):
		if int(size.get("width"))>=500:
			break

	image_url = size.get("source")

	info = flickr.photos_getInfo(photo_id=id, secret=r.get("secret"))
	page_url = info.find("photo").find("urls").find("url").text
	author = info.find("photo").find("owner").get("realname")

	encoder = getencoder("ascii")

	return encoder("<img style=\"max-height:300px\" src=\"%s\" /><br />\n<small>By <a href=\"%s\">%s</a> on flickr"%(image_url, page_url, author),"ignore")[0]

def teakittens(environ, start_response):
	from cStringIO import StringIO
	import traceback
	ret = StringIO()
	try:
		print >>ret, "<title>More tea and kittens</title>"
		print >>ret, """<h2>More tea and kittens</h2>
		Inspired by <a href="http://www.teaandkittens.co.uk/">Tea and Kittens</a>, plus
		the <a href="http://www.flickr.com/services/api/">Flickr API</a><br />"""
		print >>ret, "<table><tr><td>"
		print >>ret,get_html(tag="tea", cluster_id="teapot-china-teacup")
		print >>ret, "</td><td>"
		print >>ret,get_html(tag="kittens", cluster_id="cats-cat-kitten")
		print >>ret, "</tr></table"
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
