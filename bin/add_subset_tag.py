#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import simplejson as json
import io
from datetime import datetime
from pprint import pprint
import os
import sys
import argparse
from mysql_insert_queries import *

from twitter_mysql.utils.db import build_connection_from_configfile
from twitter_mysql.utils.configfile import ConfigArgumentParser, get_configfile_from_args
from twitter_mysql.utils.csv_helpers import SimpleCSVReader

TAG_SELECT_QUERY = """SELECT id from subset_tags where name = %s"""
TAG_CREATE_QUERY = """
    INSERT INTO subset_tags (`name`, `description`) VALUES (%s, %s)
"""
USER_TAG_CREATE_QUERY = """
    INSERT INTO user_subset_tags 
    (`subset_tag_id`,`user_id`)
    VALUES (%s, %s)"""

#
#
# functions
#
#

def get_tag_id(cursor, tag_name, create=False, description=None):
    """ Get or create the tag id. """
    cursor.execute(TAG_SELECT_QUERY, (tag_name,))
    row = c.fetchone()

    # if we got a valid one, return it
    if row is not None:
        return row[0]

    if create:
        cursor.execute(TAG_CREATE_QUERY, (tag_name, description,))
        return cursor.lastrowid

    raise Exception(
        "Tag does not exist, and you didn't specify the create option.")

#
#
# program arguments
#
#
argparser = ConfigArgumentParser(
    description="adds user ids to as subset tags")

argparser.add_argument(
    "inputfile",
    help="input csv filename")
argparser.add_argument(
    "tag",
    help="name of the subset tag to insert")
argparser.add_argument(
    "--create",
    help="create tag if it doesn't exist",
    action="store_true")
argparser.add_argument(
    "--description",
    help="description of the tag if it is inserted",
    default=None)
argparser.add_argument(
    "--limit",
    help="limit the number of lines to this value",
    type=int,
    default=None)

args = argparser.parse_args()
configfile = get_configfile_from_args(args)

# open db connection
db = build_connection_from_configfile(configfile)
c = db.cursor()


tag_id = get_tag_id(c, args.tag, args.create, args.description)
print "got tag id for", args.tag, tag_id


with SimpleCSVReader(args.inputfile) as f:
    user_ids = [(tag_id, row["user_id"]) for row in f]
    if args.limit:
        del user_ids[args.limit:]
        print len(user_ids), "user ids"
    c.executemany(USER_TAG_CREATE_QUERY, user_ids)


c.close()
db.commit()
db.close()
