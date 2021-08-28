from googleapiclient.discovery import build
from google.oauth2 import service_account
import json



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'key.json' # ----- Download this file for your project from google developer console and place in the same folder
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.
spreadsheet_id = '#####' # ----- Replace ##### with spreadsheet id

service = build('sheets', 'v4', credentials=creds)



def gsheet_names():
        # Call the Sheets API to get all worksheet names
        result = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

        sheets = set()
        for sheet in result['sheets']:
                sheets.add(sheet['properties']['title'])
        
        return (sheets)

def values_get(sheet_name):
        result1 = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=f'{sheet_name}!A1:H100').execute()
        return(result1.get('values', []))


def add_sheet(sheet_name):
        # call to create now worksheet
        request_body = {
                "requests": [{'addSheet':
                                {
                                        'properties': {
                                                'title': sheet_name
                                        }
                                }
                        }],
                "includeSpreadsheetInResponse": False,
                "responseIncludeGridData": False
        }

        result2 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()

def clear_sheet(sheet_name):
        rangeAll = f'{sheet_name}!A1:Z'
        resultClear = service.spreadsheets().values().clear( spreadsheetId=spreadsheet_id, range=rangeAll).execute()

def write_sheets(sheet_name, data):
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=f'{sheet_name}!A1', valueInputOption='USER_ENTERED', body={'values': data}).execute()
