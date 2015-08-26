#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
from tweepy.parsers import JSONParser
import requests

# temporary, but it's a pain in the ass
requests.packages.urllib3.disable_warnings()


class TweepyWrapper(object):

	"""Tweepy Wrapper."""

	def __init__(self, configfile):
		"""initialize with configfile."""

		self.configure(configfile)

	def configure(self, configfile):
		"""configure Tweepy from configfile."""

		if configfile is None:
			raise Exception("Configfile is None.")

		api_key = configfile.getValueOrRaise(
			"twitter_auth.api_key")
		api_secret = configfile.getValueOrRaise(
			"twitter_auth.api_secret")
		access_token = configfile.getValueOrRaise(
			"twitter_auth.access_token")
		access_token_secret = configfile.getValueOrRaise(
			"twitter_auth.access_token_secret")

		self.auth = tweepy.OAuthHandler(api_key, api_secret)
		self.auth.set_access_token(access_token, access_token_secret)

	def get_api(self):
		parser = JSONParser()
		return tweepy.API(self.auth, parser=parser)