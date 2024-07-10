import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authenticate_gspread(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(credentials)
    return client


def upload_dataframe_to_google_sheet(dataframe, spreadsheet_name, worksheet_name, json_keyfile):
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

    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=dataframe.shape[0] + 1, cols=dataframe.shape[1])

    # Convert DataFrame to list of lists and update the worksheet
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


# Main execution flow
# Replace 'path_to_credentials.json' with the path to your credentials JSON file
# Replace 'repositories.csv' with the name of your CSV file
# Replace 'Your Spreadsheet Name' and 'Your Worksheet Name' with your desired names

csv_file = 'repositories.csv'
spreadsheet_name = 'CAOS-REPOSITORIES'
worksheet_name = 'script_data'
json_keyfile = 'app/google_credentials.json'

# Read CSV into DataFrame
df = pd.read_csv(csv_file)

# Upload DataFrame to Google Sheets
upload_dataframe_to_google_sheet(df, spreadsheet_name, worksheet_name, json_keyfile)
