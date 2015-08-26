#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import time
import datetime
from twitter_mysql.utils.db import build_connection_from_configfile
from twitter_mysql.utils.configfile import ConfigArgumentParser, get_configfile_from_args
from twitter_mysql.utils.twitter import TweepyWrapper
import os
import simplejson as json
import glob
import re
from tweepy.error import TweepError

# modified from http://stackoverflow.com/a/312464
def chunk(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


#
#
# program arguments
#
#
argparser = ConfigArgumentParser(description="dump user ids in database")
argparser.add_argument("inputfile", help="input filename (user ids one per line)")
argparser.add_argument("outdir", help="outputdirectory")
args = argparser.parse_args()
configfile = get_configfile_from_args(args)

# tweepy config
tw = TweepyWrapper(configfile)
api = tw.get_api()

ids = None
with io.open(args.inputfile, "r") as f:
	ids = set([int(id) for id in f.readlines()])

print len(ids), " accounts to lookup"

# remove ids if the file exists already
out_path = os.path.join(args.outdir, "*.json")
files = glob.glob(out_path)
id_regex = re.compile("(\d*)\.json", re.I)

for file_path in files:
	fn = os.path.basename(file_path)
	result = id_regex.match(fn)
	if result is not None:
		try:
			id = int(result.group(1))
			ids.discard(id)
		except:
			pass



print len(ids), " accounts to lookup after culling"


# chunk up the results
req_chunks = list(chunk(list(ids), 100))
batches = list(chunk(req_chunks, 60))

for b in range(len(batches)):
	print "Batch %d of %d " % (b, len(batches))
	batch = batches[b]
	for i in range(len(batch)):
		req_data = batch[i]
		#print i, len(req_data)
		try:
			results = api.lookup_users(user_ids=req_data, include_entities=True)

			print len(results)


			if isinstance(results, list):
				for r in results:
					if 'id' in r:
						id = r['id']
						filename = "%d.json" % (id)
						filepath = os.path.join(args.outdir, filename)
						with io.open(filepath, "w") as f:
							f.write(unicode(json.dumps(r)) + "\n")
					else:
						print "id not present in result"
						print json.dumps(r)
			else:
				print "results is not a list"
				print json.dumps(r)
		except TweepError, e:
			print "ERROR: ", e


	# sleep for window duration
	time.sleep(15*60)

