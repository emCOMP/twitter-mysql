#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import io
from twitter_mysql.utils.db import add_db_args, get_db_mysql_connection

#
#
# program arguments
#
#
parser = argparse.ArgumentParser(description='user id dumper')
parser.add_argument('filename', help="output file")
add_db_args(parser)
args = parser.parse_args()

# open db connection
db = get_db_mysql_connection(args)
c=db.cursor()

# run query
results = c.execute("""select id from users""")

with io.open(args.filename, "w") as f:
	for row in c:
		f.write(unicode(row[0]) + "\n")

c.close()
db.close()

