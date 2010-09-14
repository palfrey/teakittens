More Tea and Kittens
====================

Originally, there was `Tea and Kittens <http://www.teaandkittens.co.uk/>`_. However,
it had a few flaws, namely not enough Tea, and not enough Kittens. So, I built
a better one. This ties into the Flickr API for a specified set of keywords and
generates a page with random images from those keywords. The index.py supplied here
picks keywords such that we get tea and kitten pictures, but you could use it for
anything else (coffee and puppies for example).

Technical details
-----------------
It uses Python pickle files to store the picture URLs, as repeatedly querying the Flickr
API is slow, and this way we get to have a larger pool of pictures to pick from. I started
off using the cluster API, but that only gives you 24 pictures via the API (v.s. 1000s on
the website...), and the tag API seems to not know the difference between exclude and include
tags, so now the tags you hand in are just concatenated and dumped into the plain text search.

To initialise a copy of the site, do the following:

1. Create a file called "secrets" that contains two lines: your Flickr API key, and 
   Flickr API secret

2. Run index.py locally repeatedly (i.e. "python index.py") until it completes instantly.
   If you're lucky, it'll just run through the first time, but sometimes the Flickr API
   breaks and you get a timeout and we throw an exception. We cache everything as we go
   through, so sooner or later it'll get all the data. After this point, no more queries
   to the Flickr API are needed (as we're caching everything in some .pickle files), but
   ~300 queries are needed in this stage, hence the possible problems.

3. Copy the contents of this folder to your website.

4. Provided you've got mod_python or equivalent setup to run .py files, all should now work!
