import flickrapi
import pickle

(api_key, secret) = [x.strip() for x in file("secrets").readlines()]
flickr = flickrapi.FlickrAPI(api_key)

def get_list(count=20, tags=[]):
	pklname = "photos-%s.pickle"%("-".join(tags))
	
	ids = None
	photos = {}
	try:
		f = file(pklname,"rb")
		ids = pickle.load(f)
		if len(ids)<count:
			ids = None
		photos = pickle.load(f)
	except IOError:
		pass
	except EOFError:
		pass

	if ids == None:
		ids = [photo.get("id") for photo in flickr.photos_search(text=" ".join(tags),per_page=count).find("photos")]
		
		f = file(pklname,"wb")
		pickle.dump(ids, f)
		pickle.dump(photos, f)
		f.close()
	
	got = 0
	for id in ids:
		if id not in photos:
			print id
			sizes = flickr.photos_getSizes(photo_id=id)
			for size in list(sizes.find("sizes")):
				if int(size.get("width"))>=500:
					break

			image_url = size.get("source")

			info = flickr.photos_getInfo(photo_id=id)
			page_url = info.find("photo").find("urls").find("url").text
			author = info.find("photo").find("owner").get("realname")

			print image_url,author,page_url
			photos[id] = {"image":image_url, "author":author, "page":page_url}

			f = file(pklname,"wb")
			pickle.dump(ids, f)
			pickle.dump(photos, f)
			f.close()
		got +=1
		if got == count:
			break

	return photos

if __name__ == "__main__":
	print get_list(count=5,tags=("cats","cat","kittens"))

