#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import codecs
import csv
import re



def csv_escape(val):
    #str.replace("\"", "\\\"")
    val = re.sub(u'[' + string.whitespace + u']', u' ', val)

    if u'"' in val or ',' in val:
        return u'"""' + val + u'"""'

    return val


class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.encoding = encoding
        self.reader = csv.DictReader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return {k: unicode(v, "utf-8") for k, v in row.iteritems()}

    def __iter__(self):
        return self


class SimpleCSVWriter(object):
    """ Simple CSV Writer."""

    def __init__(
            self, filename,
            encoding="utf8", write_bom=True):
        self.file = codecs.open(filename, "w+", encoding=encoding)
        if write_bom:
            self.file.write(u'\ufeff')

    def __enter__(self):
        return self

    def __exit___(self, type, value, traceback):
        if self.file:
            self.file.close()

    def writeRow(self, array_values):
        self.file.write(u",".join(array_values) + "\n")

    def writeDict(self, _dict):
        headers = sorted(_dict.values()[0].keys())
        self.writeRow(headers)

        for k, v in _dict.iteritems():
            row_vals = [csv_escape(unicode(v[col])) for col in headers]
            self.writeRow(row_vals)


class SimpleCSVReader(object):
    """
    A simple wrapper for a unicode dictionary reader.
    """

    def __init__(self, filename):
        """ open file """

        self.file = open(filename, "r")
        self.name = os.path.basename(filename)
        self.csv = UnicodeDictReader(self.file)

    def __enter__(self):
        return self.csv

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """ close the file """
        if self.file is not None:
            self.file.close()
