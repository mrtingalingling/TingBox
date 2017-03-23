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


class DataIO: 

	today_str = str(date.today()).replace("-", "")
	file_dir = dirname(abspath(__file__))
	main_dir = file_dir.split('git')[0]

	def __init__(self, *args, **kwargs):
		super().__init__(self, config=None, *args, **kwargs)

		self.parse_args = self._parse_args()

		if not config: 
			self.file_path = input('Please enter the location of your file: ')
		else:
			self.config = config
			try: 
				self.file_paths = config.get('file_paths')
			except Exception as e: 
				log.error('Error! No path found.')
				return 

		if 'dbname' in self.file_paths:
			log.info('SQL Database access requested instead, checking DB credential.')
			self.psql_login_check(self.file_paths)

	def _parse_args(self):
		parser = ArgumentParser()
		parser.add_argument('--filename', required=True, help="Filename.")
		parser.add_argument('--file-type', required=True, help="File Type.")
		# parser.add_argument('--debug', required=False, action='store_true', help="Log in debug mode.")
		# parser.add_argument('--querysrch', required=False, action='store_true', nargs='+', help="Initiate search of the site entered.")
		# if both querysrch and tags are there, use parser.parse_args('args'.split())
		args, trash = parser.parse_known_args()

		return args

	def parse_file(self):
		for file_path in self.file_paths:
			file_type = file_path.split('.')[1]
			try: 
				if file_type == 'csv': 
					return read_csv(file_type)
				elif 'xls' in file_type: 
					return read_xlsx(file_path)
				elif 'txt' in file_type: 
					return read_txt(file_path)
				else: 
					return None 
			except EXCEPTION as e: 
				log.error('Error! Unknown file type, please select only Excel, CSV, or Postgres Login.')

	def log_data_psql(self, args_dict, db_name): 
		'''This will be a place holder to customized log_data_psql fcn'''
		with psycopg2.connect("dbname=test_db").cursor() as cur: 
			args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in args_dict)
			cur.execute("INSERT INTO table VALUES " + args_str) 

	def read_csv(file_path):
		csv_data = csv.reader(file_path, delimiter=',')
		csv_data = list(csv_data)

		return data_set 

	def save_to_csv(data_set):  # Need to check if is a better way, and not sure if this is the way to add data into CSV 
		csv_file = open(filename + '.csv', 'wb')
		wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

		for row_values in data_set:
			wr.writerow(row_values)

		csv_file.close()

	def read_xlsx(file_path, sheet_names=None):
		#  xlsx is expected to have xls in the string
		wb = xlrd.open_workbook(file_path)
		sh = wb.sheet_by_name(sheet_names)
		custom_xlsx_rd(sh)

	def custom_xlsx_rd():
		# Organize data,  placeholder method needed 
		data_class = {}
		data_subclass = {}
		data_set = {}
		for rownum in xrange(sh.nrows):
			if rownum > 1:
				colnum = 0
				data = {}
				for ds in sh.row_values(rownum):
					data[data_subclass[colnum]] = ds
					colnum += 1
				data_set[data['State']] = data
			elif rownum == 1: 
				data_subclass = sh.row_values(1)
				data_subclass[0] = 'State'
				data_subclass = tuple(data_subclass)
			elif rownum == 0:
				for dc in sh.row_values(0): 
					data_class[dc] = {}

		return data_set

	def read_txt(self, filename):
		key_phrase = ''
		expression = ''

		if isfile(filename) is True:
			with open(filename, 'rb') as file_content:
				file_content_readlines = file_content.readlines()

				'''Still need to figure out how to set up a hook'''
				custom_txt_rd(file_content_readlines)

	def custom_txt_rd(file_content_readlines):
		'''Placeholder method needed''' 
		# Read the last line
		for line in reversed(file_content_readlines):
			if key_phrase in line:
				# Do something fancy AF
				break
			else:
					# Do something else fancy AF 
				break
		# Base on that fancy thing, choose what to do 
		if True:
			log.info('Reading text file')
			for row in file_content_readlines:
				# Search for expression 
				if expression in row:
					matching_expression = re.search('(?<=@)\w+', row).group(0)
					if matching_expression in expression_dict:
						# Do something fancy 
						keys = [k for k in table_dict.keys()]
						content = [tuple(str(v) for k, v in table_dict.iteritems())]


if __name__ == '__main__':
	# parsed_args = _parse_args()

	filename = '2016 November General Election.xlsx'
	data_set = read_xlsx(filename)
	print data_set


### Reference: 
# http://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python	
# http://stackoverflow.com/questions/1038160/data-structure-for-maintaining-tabular-data-in-memory

'''This is a reference python/PSQL fucntion'''
# with psycopg2.connect(db_login).cursor() as cur: 
# 	args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in args_dict)
# 	query = "INSERT INTO table VALUES " + args_str
# 	cur.execute(query) 
# 	cur.fetchall()
