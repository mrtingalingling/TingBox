#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting
Get all stock information'''
import logging
# import traceback
from argparse import ArgumentParser
# from pprint import pprint
# from subprocess import call
# from os.path import join, abspath, dirname, isfile
from sshtunnel import SSHTunnelForwarder
# from sp500 import SP500
import imp
import psycopg2

log = logging.getLogger(name=__file__)


class TingLabAccess:

	def __init__(self, *args, **kwargs):
		# super().__init__(self, config=None, *args, **kwargs)

		self.parse_args = self._parse_args()

		amaho_access_dir = '/Users/tto'
		try:
			if not amaho_access_dir:
				amaho_access_dir = '/home/ting'
			amaho_access = imp.load_source('amaho_access', '{}/Dropbox/script_configs/amaho_access.py'.format(amaho_access_dir)).amaho_access
		except Exception as e:
			print(e)
			print('amaho_access not found')
		db_name = amaho_access['db_name']

		PORT = 5432
		REMOTE_USERNAME = amaho_access['REMOTE_USERNAME']
		REMOTE_PASSWORD = amaho_access['REMOTE_PASSWORD']
		REMOTE_HOST = amaho_access['REMOTE_HOST']
		REMOTE_SSH_PORT = 22
		with SSHTunnelForwarder(
			(REMOTE_HOST, REMOTE_SSH_PORT),
			ssh_username=REMOTE_USERNAME,
			ssh_password=REMOTE_PASSWORD,
			remote_bind_address=('localhost', PORT),
			local_bind_address=('localhost', PORT)):
			with psycopg2.connect(db_name) as conn:
				self.conn = conn
				self.cur = self.conn.cursor()

	def _parse_args(self):
		parser = ArgumentParser()
		args, trash = parser.parse_known_args()

		return args


if __name__ == '__main__':
	pass
