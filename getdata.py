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

		if not config is None: 
			self.file_path = input('Please enter the location of your file: ')
		else:
			self.config = config
			try: 
				self.file_path_list = config.get('file_path')
			except Exception as e: 
				log.error('Error! No path found.')
				return 

		for file_path in file_path_list:
			try: 
				parse_file(file_path)
			except EXCEPTION as e: 
				log.error('Error! Unknown file type, please select only Excel, CSV, or Postgres Login.')

	def _parse_args(self):
		parser = ArgumentParser()
		parser.add_argument('--filename', required=True, help="Filename.")
		parser.add_argument('--file-type', required=True, help="File Type.")
		# parser.add_argument('--debug', required=False, action='store_true', help="Log in debug mode.")
		# parser.add_argument('--querysrch', required=False, action='store_true', nargs='+', help="Initiate search of the site entered.")
		# if both querysrch and tags are there, use parser.parse_args('args'.split())
		args, trash = parser.parse_known_args()

		return args

	def parse_file(file_path):
		file_type = file_path.split('.')[1]
		if file_type == 'csv': 
			return True  # read_csv(file_type)
		elif 'xls' in file_type: 
			return True  # read_xlsx(file_path)
		elif 'txt' in file_type: 
			return True  # read_xlsx(file_path)
		elif file_type is None and 'dbname' in file_path: 
			return True  # read_db(file_path)
		else: 
			return None 

	def read_csv(filename, sheet_names='Turnout Rates'):

		# file_path = join(main_dir, filename)

		csv_data = csv.reader(file_path, delimiter=',')
		csv_data = list(csv_data)

		return data_set 

	def save_xlsx_to_csv(filename, xlsx_sh, save_to_csv=True): 
		filename = filename.split('.')[0]
		sh = xlsx_sh

		if save_to_csv is True: 
			csv_file = open(filename + '.csv', 'wb')
			wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

			for rownum in xrange(sh.nrows):
				wr.writerow(sh.row_values(rownum))

			csv_file.close()

	def read_xlsx(filename, sheet_names='Turnout Rates'):
		#  xlsx is expected to have xls in the string
		file_path = join(main_dir, filename)
		wb = xlrd.open_workbook(file_path)
		sh = wb.sheet_by_name(sheet_names)

		save_xlsx_to_csv(filename, sh, save_to_csv=False)

		# Organize data 
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

	def log_data_to_psql(args_dict, db_name='test_db'): 
		db_name = 'dbname=' + db_name
		'''This will be a place holder to customized log_data_psql fcn'''
		with psycopg2.connect(db_name).cursor() as cur: 
			args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in args_dict)
			cur.execute("INSERT INTO table VALUES " + args_str) 

	def read_db(query, db_name='test_db'):
		db_name = 'dbname=' + db_name
		if 'SELECT' not in query.upper():
			return 

		with psycopg2.connect("dbname=test_db").cursor() as cur: 
			cur.execute(query) 

		return cur.fetchall()

	def read_text_file(filename):
		key_phrase = ''
		expression = ''

		if isfile(filename) is True:
			with open(filename, 'rb') as file_content:
				file_content_readlines = file_content.readlines()
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

	# if parsed_args.filename: 
		# if parsed_args.file_type == 'txt': 
		# 	read_text_file(parsed_args.filename)
		# if parsed_args.file_type == 'tbl': 
		# 	read_table(parsed_args.filename)
		# if parsed_args.file_type == 'db': 
		# 	read_db(parsed_args.filename)

### Reference: 
# http://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python	
# http://stackoverflow.com/questions/1038160/data-structure-for-maintaining-tabular-data-in-memory
