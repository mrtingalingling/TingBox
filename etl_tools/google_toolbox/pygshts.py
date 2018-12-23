#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Ting
Google Sheet I/O
'''

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# import imp
# from sshtunnel import SSHTunnelForwarder
import logging
from tinglab_access import TingLabAccess
import argparse

log = logging.getLogger(name=__file__)

class GoogleSheet:
	try:
		import argparse
		flags, unknown_flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args()
	except ImportError:
		flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'  # .readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python IO'

    def __init__(self, *args, **kwargs):
        # super().__init__(self, config=None, *args, **kwargs)
		self.gsht_service = self.check_credentials()
        for k, v in kwargs.iteritems():
            self.k = v

        self.parse_args = self._parse_args()

	def check_credentials(self):
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
		service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

		return service

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        try:
            CLIENT_SECRET_FILE = input('Please enter the location of your CLIENT_SECRET_FILE: ')
            print(CLIENT_SECRET_FILE)
        except Exception as e:
            log.warning(e)
            if not CLIENT_SECRET_FILE:
                log.info('CLIENT_SECRET_FILE not found, exiting.')
                return

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

	# Added Function #
	def gsht_update_body_builder(self, sheet_title_string):
		# https://developers.google.com/sheets/api/guides/batchupdate
		# Config Sheet Properties
		SheetProperties = {
			# "sheetId": sheetId_number,
			"title": sheet_title_string,
			# "index": sheet_index_number
		}

		AddSheetRequest = {
			# {object(SheetProperties)}
			"properties": SheetProperties
		}

		add_sheet_request = [
			{
				# {object(AddSheetRequest)}
				"addSheet": AddSheetRequest
			},
			# UpdateCellsRequest
		]

		request_body = {
			"requests": add_sheet_request,
		}

		return request_body

	def gsht_values_body_builder(self, value_input_option, value_range_body):
		# https://developers.google.com/sheets/api/guides/values
		values_batchupdate_body = {
			"valueInputOption": value_input_option,
			"data": [value_range_body]
		}

		return values_batchupdate_body

	def gsht_body_builder(self, action, data_values=[[]], rangeName='', sheet_title_string='Test_Tab', value_input_option='USER_ENTERED'):
		value_range_body = {
			"range": rangeName,
			"majorDimension": "ROWS",
			"values": data_values
		}

		if action == 'AddSheet':
			return self.gsht_update_body_builder(sheet_title_string)
		elif action == 'Write':
			return self.gsht_values_body_builder(value_input_option, value_range_body)
		elif action == 'Add':
			return {"values": data_values}

	def gsht_update(self, spreadsheetId, action, data_values=[[]], rangeName='', sheet_title_string='Test_Tab', value_input_option='USER_ENTERED'):
		if not rangeName:
			rangeName = sheet_title_string

		data_body = self.gsht_body_builder(action, data_values, rangeName, sheet_title_string)

		try:
			if action == 'AddSheet':
				# Create New Sheet to SpreadSheet
				response = self.g_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=data_body).execute()
				print(response)
			elif action == 'Write':
				# Add Values to Sheet
				response = self.g_service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=data_body).execute()
				print(response)
			elif action == 'Read':
				# Read Values to Sheet
				response = self.g_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, range=rangeName).execute()
				print(response)
			elif action == 'Add':
				# Append Values to Sheet
				response = self.g_service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option, body=data_body).execute()
				print(response)
		except Exception as e:
			print(e)


if __name__ == '__main__':
    # tinglab_access_dir = '/Users/tto'
    # try:
    #     if not tinglab_access_dir:
    #         tinglab_access_dir = '/home/ting'
    #     tinglab_access = imp.load_source('amaho_access', '{}/Dropbox/script_configs/amaho_access.py'.format(tinglab_access_dir)).tinglab_access
    # except Exception as e:
    #     print(e)
    #     print('amaho_access not found')
    # db_name = tinglab_access['db_name']

    # PORT = 5432
    # REMOTE_USERNAME = tinglab_access['REMOTE_USERNAME']
    # REMOTE_PASSWORD = tinglab_access['REMOTE_PASSWORD']
    # REMOTE_HOST = tinglab_access['REMOTE_HOST']
    # REMOTE_SSH_PORT = 22
    # with SSHTunnelForwarder(
    #     (REMOTE_HOST, REMOTE_SSH_PORT),
    #     ssh_username=REMOTE_USERNAME,
    #     ssh_password=REMOTE_PASSWORD,
    #     remote_bind_address=('localhost', PORT),
    #         local_bind_address=('localhost', PORT)):
    #     with psycopg2.connect(db_name) as conn:
    g_sht = GShtConn(TingLabAccess)

    '''Insert custom function'''
    spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    rangeName = 'Class Data!A2:E'
    result = g_sht.service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


	"""Shows basic usage of the Sheets API.

	Creates a Sheets API service object and prints the names and majors of
	students in a sample spreadsheet:
	https://docs.google.com/spreadsheets/d/1f9qY7VW8mwIopLVJzmKKzTD8Qxxt33rcJOrbH-Yx-bs/edit#gid=0
	"""
	gsht = GoogleSheet()
	service = gsht.gsht_service

	spreadsheetId = '1f9qY7VW8mwIopLVJzmKKzTD8Qxxt33rcJOrbH-Yx-bs'
	rangeName = 'Sheet2!A2:E'
	result = service.spreadsheets().values().get(
		spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])

	if not values:
		print('No data found.')
	else:
		print('Name, Major:')
		max_row_size = 1
		for row in values:
			max_row_size = len(row) if len(row) > max_row_size else max_row_size
			if len(row) == 0:
				continue
			for rn in range(max_row_size):
				if rn > len(row):
					row[rn] = ''
			# Print columns A and E, which correspond to indices 0 and 4.
			print('%s, %s' % (row[0], row[4]))

	value_input_option = 'USER_ENTERED'
	value_range_body = {'values': [['hahaha', '5678'], ['lolol']]}
	request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option, body=value_range_body)
	response = request.execute()
	print(response)

# https://bl.ocks.org/mbostock/4063550
