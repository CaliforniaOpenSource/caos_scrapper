import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authenticate_gspread(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)
    return client


def upload_csv_to_google_sheet(csv_file, spreadsheet_name, worksheet_name, json_keyfile):
    client = authenticate_gspread(json_keyfile)

    # Open the Google Sheet (it will be created if it does not exist)
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        spreadsheet.del_worksheet(worksheet)
    except gspread.WorksheetNotFound:
        pass

    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)

    # Read the CSV file and upload its content to the Google Sheet
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row_index, row in enumerate(reader):
            for col_index, cell in enumerate(row):
                worksheet.update_cell(row_index + 1, col_index + 1, cell)


# Replace 'path_to_credentials.json' with the path to your credentials JSON file
# Replace 'repositories.csv' with the name of your CSV file
# Replace 'Your Spreadsheet Name' and 'Your Worksheet Name' with your desired names
upload_csv_to_google_sheet('repositories.csv', 'CAOS-REPOSITORIES', 'script_data',
                           'app/google_credentials.json')
