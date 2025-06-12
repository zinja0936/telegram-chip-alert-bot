import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth_google():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    return gspread.authorize(creds)

def get_sheet_data(sheet_url):
    gc = auth_google()
    sheet = gc.open_by_url(sheet_url).sheet1
    return sheet.get_all_values()

def update_sheet_note(sheet_url, row, col, note):
    gc = auth_google()
    sheet = gc.open_by_url(sheet_url).sheet1
    sheet.update_cell(row, col, note)
