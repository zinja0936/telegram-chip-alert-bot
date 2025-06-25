import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth_google():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # 從環境變數中讀取 JSON 金鑰字串，轉為 dict
    google_json_str = os.environ.get("GOOGLE_JSON")
    creds_dict = json.loads(google_json_str)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def get_sheet_data(sheet_id):
    gc = auth_google()
    sheet = gc.open_by_key(sheet_id).sheet1
    return sheet.get_all_values()

def update_sheet_note(sheet_id, row, col, note):
    gc = auth_google()
    sheet = gc.open_by_key(sheet_id).sheet1
    sheet.update_cell(row, col, note)
