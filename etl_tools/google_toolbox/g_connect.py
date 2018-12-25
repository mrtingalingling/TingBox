#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Author: Ting
Google Sheet I/O'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
# https://developers.google.com/identity/protocols/OAuth2ServiceAccount
# https://github.com/burnash/gspread/blob/c0a5a6d83083c467a647ab91bf1caaa1f829b5c7/tests/test.py
from functools import wraps, partial
from apiclient.http import MediaIoBaseDownload
import io, csv, logging, sys, traceback


class GoogleAPIConnect:
	try:
		import argparse
		flags, unknown_flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args()
	except ImportError:
		flags = None

	# If modifying these scopes, delete your previously saved credentials
	# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
	SHEET_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'  # .readonly'
	DRIVE_SCOPES = 'https://www.googleapis.com/auth/drive'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'GoogleSheet_DB_Sync'

	def __init__(self):
		self.gsht_service, self.gdrv_service = self.get_credentials()

	def get_credentials(self):
		# The file token.json stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		sheet_store = file.Storage('sheet_token.json')
		drive_store = file.Storage('drive_token.json')
		sheet_creds = sheet_store.get()
		drive_creds = drive_store.get()
		if not sheet_creds or sheet_creds.invalid:
			sheet_flow = client.flow_from_clientsecrets('credentials.json', self.SHEET_SCOPES)
			sheet_creds = tools.run_flow(sheet_flow, sheet_store)
		if not drive_creds or drive_creds.invalid:
			drive_flow = client.flow_from_clientsecrets('credentials.json', self.DRIVE_SCOPES)
			drive_creds = tools.run_flow(drive_flow, drive_store)
		sheet_service = build('sheets', 'v4', http=sheet_creds.authorize(Http()))
		drive_service = build('drive', 'v3', http=drive_creds.authorize(Http()))

		return sheet_service, drive_service

	@classmethod
	def google_sheet_read(cls, spreadsheetId, rangeName, access='r'):
		if access == 'w':
			print("Can't change to write privilege yet. Sorry :(")
			return

		gsht_service = cls().gsht_service
		# gdrv_service = cls().gdrv_service

		result = gsht_service.spreadsheets().values().get(
			spreadsheetId=spreadsheetId, range=rangeName).execute()
		return result


class GoogleAPIFunction(GoogleAPIConnect):
	def __init__(self):
		super()

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
				response = self.gsht_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=data_body).execute()
				print(response)
			elif action == 'Write':
				# Add Values to Sheet
				response = self.gsht_service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=data_body).execute()
				print(response)
			elif action == 'Read':
				# Read Values to Sheet
				response = self.gsht_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, range=rangeName).execute()
				print(response)
			elif action == 'Add':
				# Append Values to Sheet
				response = self.gsht_service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option, body=data_body).execute()
				print(response)
		except Exception as e:
			print(e)


from functools import wraps, partial


class DecorableHooks:

	@classmethod
	def hook_func(prefunction):
		def decorator_func(cls, f):
			'''Add custom function to the decorator_dict, example hook name: f.__name__ + _hook'''
			cls.decorator_dict = {}
			# @hook_func

			def wrapper(*args, **kwds):
				print('Add custom function the decorator_dict')
				cls.decorator_dict = {prefunction.__name__: f}
				return f(*args, **kwds)
			return wrapper
		return decorator_func

	@classmethod
	def decorable(cls, f):
		'''Add customization to decorable function result'''
		cls.decorator_dict
		# @decorable

		@wraps(f)
		def wrapper(*args, **kwds):
			if f.__name__ in cls.decorator_dict.keys().split('_hook')[0]:
				return cls.decorator_dict[f.__name__](f(*args, **kwds))
			else:
				print(f.__name__, ' is not implemented because the decorated function is not found, please check again.')
		return wrapper


def google_drive_download(drive_service, file_id='1lpOFpru54DTiCuV8bfAKVrHFTa9f3h7x'):
	# Download Files
	request = drive_service.files().get_media(fileId=file_id)
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print("Download %d%%." % int(status.progress() * 100))
	return fh.getvalue()


def main():
	"""Shows basic usage of the Sheets API.

	Creates a Sheets API service object and prints the names and majors of
	students in a sample spreadsheet:
	https://docs.google.com/spreadsheets/d/1f9qY7VW8mwIopLVJzmKKzTD8Qxxt33rcJOrbH-Yx-bs/edit#gid=0
	"""
	google_api = GoogleAPIConnect()
	drive_service = google_api.gdrv_service
	# sheet_service = google_api.gsht_service

	spreadsheetId = '1U0LsfdZlv217Di9h65P4IFAu--3qHEL2owQhlvcWM-w'
	rangeName = 'Sheet1'

	# Get sample data
	downloaded_file = google_drive_download(drive_service)

	# value_input_option = 'USER_ENTERED'
	# value_range_body = {'values': [['hahaha', '5678'], ['lolol']]}
	# request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option, body=value_range_body)
	# response = request.execute()
	# print(response)

	# result = sheet_service.spreadsheets().values().get(
	# 	spreadsheetId=spreadsheetId, range=rangeName).execute()
	# values = result.get('values', [])

	# if not values:
	# 	print('No data found.')
	# else:
	# 	print('Name, Major:')
	# 	max_row_size = 1
	# 	for row in values:
	# 		max_row_size = len(row) if len(row) > max_row_size else max_row_size
	# 		if len(row) == 0:
	# 			continue
	# 		for rn in range(max_row_size):
	# 			if rn > len(row):
	# 				row[rn] = ''
	# 		# Print columns A and E, which correspond to indices 0 and 4.
	# 		print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
	main()

# https://bl.ocks.org/mbostock/4063550
