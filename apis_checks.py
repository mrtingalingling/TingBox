#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting'''
import logging
import traceback
from argparse import ArgumentParser
from datetime import date
from pprint import pprint
from subprocess import call
import re
from collections import defaultdict
from os.path import join, abspath, dirname, isfile
import csv
import xlrd
# import matplotlib.pyplot as plt
import psycopg2

log = logging.getLogger(name=__file__)


class CommonAPIs: 

	def run_api(self): 
		'''Going to add some API access function here'''

		return 


# Google Sheet API
		if self.config.get('g_doc'): 
			# Create client and spreadsheet objects
			password = getpass.getpass()
			gs = Client(self.config['g_doc'].get('email'), password)
			ss = Spreadsheet(spreadsheet_id)
			
			# Request a file-like object containing the spreadsheet's contents
			csv_file = gs.download(ss)
			
			# Parse as CSV and print the rows
			for row in csv.reader(csv_file):
				print ", ".join(row)

# RESTAPI 

# Github API 

