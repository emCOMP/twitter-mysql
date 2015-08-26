#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from twitter_mysql.utils.db import build_connection_from_configfile
from twitter_mysql.utils.configfile import ConfigArgumentParser, get_configfile_from_args

#
#
# program arguments
#
#
argparser = ConfigArgumentParser(description="dump user ids in database")
argparser.add_argument("filename", help="output filename")
args = argparser.parse_args()
configfile = get_configfile_from_args(args)

# open db connection
db = build_connection_from_configfile(configfile)
c=db.cursor()

# run query
results = c.execute("""select id from users""")

with io.open(args.filename, "w") as f:
	for row in c:
		f.write(unicode(row[0]) + "\n")

c.close()
db.close()

