#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import getpass


def add_db_args(parser):
	"""add database arguments to argparser object."""

	parser.add_argument('host', help='host')
	parser.add_argument('database', help='database name')
	parser.add_argument('username', help="username")
	parser.add_argument('--db-encoding', default="utf8mb4", help="database encoding")
	parser.add_argument('-p', '--password', help="password for database. if not specified, will prompt.")


def get_db_password(args):
	"""get db password from args or falls back to manual input with getpass."""
	if args.password is None:
		return getpass.getpass("Enter password for %s@%s (%s) : "%(args.username, args.host, args.database))

	return None

def get_db_mysql_connection(args, password=None):
	"""creates database connection from argparser args object. 
	will call get_db_password if not specified."""
	if password is None:
		password = get_db_password(args)

	db=MySQLdb.connect(args.host, args.username, password, args.database, charset='utf8mb4', use_unicode=True)
	return db

def build_connection_from_configfile(configfile):
	"""builds database connection from configfile."""

	# throw exception if configfile is invalid
	if configfile is None:
		raise Exception("configfile is None.")

	# parse args
	host = configfile.getValue("database.host", default="localhost")
	database = configfile.getValueOrRaise(
		"database.database",
		error_message="A database name must be specified in the config file.")
	user = configfile.getValue("database.user", default="root")
	port = configfile.getValue("database.port", default=3306)
	password = configfile.getValue("database.password", default="")
	charset = configfile.getValue("database.charset", default="utf8mb4")

	# create connection
	db = MySQLdb.connect(host, user, password, 
			database, port=port, charset=charset, use_unicode=True)

	return db
