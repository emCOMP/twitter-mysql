#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import io
from datetime import datetime
from pprint import pprint
import os
import sys
import argparse
import getpass
import csv
import codecs





#
#
# program arguments
#
#
parser = argparse.ArgumentParser(description='whatevs')
parser.add_argument('host', help='host')
parser.add_argument('database', help='database name')
parser.add_argument('username', help="username")
parser.add_argument('-l', '--limit', help="limit", type=int, default=0)
#parser.add_argument('-o', '--output', help="outfile")
parser.add_argument('-f', '--filename', help="input file")
parser.add_argument('-p', '--password', help="password for database. if not specified, will prompt.")
parser.add_argument('--port', help="mysql port", default=3306, type=int)
args = parser.parse_args()


if args.password is None:
	password = getpass.getpass("Enter password for %s@%s (%s) : "%(args.username, args.host, args.database))
else:
	password = args.password



db=MySQLdb.connect(args.host, args.username, password, args.database, charset='utf8mb4', use_unicode=True, port=args.port)
c=db.cursor()


affiliations = {}
account_types = {}

values = []

account_type_values = []
affiliation_values = []

#
# open CSV file
#

with  open(args.filename, "rt") as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		user_id_str = str.strip(row["user_id"])

		if not user_id_str:
			continue

		user_id = int(user_id_str)
		affiliation = str.strip(row["Cleaned_org_affiliation"]).lower()
		account_type = str.strip(row["account_type"]).lower()

		a_id = None
		if affiliation:
			if affiliation not in affiliations:
				c.execute(
					"INSERT INTO account_affiliations (`name`, `description`, `set_id`) values (%s,%s,%s)",
					(affiliation, affiliation, 2))
				a_id = c.lastrowid
				#a_id = len(affiliations) + 1
				affiliations[affiliation] = a_id
			else:
				a_id = affiliations[affiliation]
		else:
			affiliation = None

		acc_id = None
		if not account_type:
			account_type = affiliation

		if account_type:
			if account_type not in account_types:
				c.execute(
					"INSERT INTO account_types (`name`, `description`, `set_id`) values (%s,%s,%s)",
					(account_type, account_type, 3))				
				acc_id = c.lastrowid
				#acc_id = len(account_types) +1
				account_types[account_type] = acc_id
			else:
				acc_id = account_types[account_type]
		else:
			account_type = None


		#print "%d,%s,%s,%s,%s"%(
		#	user_id, 
		#	affiliation, a_id,
		#	account_type, acc_id)

		if a_id is not None and user_id is not None:
			affiliation_values.append((user_id, a_id))
		if acc_id is not None and user_id is not None:
			account_type_values.append((user_id, acc_id))

print "\naccount_types:"
for k,v in affiliations.iteritems():
	print k,v



print "\naffiliations:"
for k,v in account_types.iteritems():
	print k,v


print "inserting %d user_account_affiliations"%(len(affiliation_values))
c.executemany("""INSERT INTO user_account_affiliations (`user_id`, `account_affiliation_id`) VALUES (%s,%s)""", affiliation_values)


print "inserting %d user_account_types"%(len(account_type_values))
c.executemany("""INSERT INTO user_account_types (`user_id`, `account_type_id`) VALUES (%s,%s)""", account_type_values)


c.close()

db.commit()
db.close()


