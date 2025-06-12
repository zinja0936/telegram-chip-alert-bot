import os, datetime, requests
from auth_google import get_sheet_data, update_sheet_note
TOKEN = os.getenv("FINMIND_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

def get_chip(stock_id, date):
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {"dataset":"TaiwanStockInstitutionalInvestorsBuySell","data_id":stock_id,"start_date":date,"token":TOKEN}
    r = requests.get(url, params=params)
    return r.json().get("data", [])

def generate_note(data):
    if not data: return "無資料"
    buy = [d for d in data if d["buy"] > d["sell"]]
    if len(buy) >= 3: return "投信連3買"
    if data[-1]["foreign_investors_buy"] > data[-1]["foreign_investors_sell"]: return "外資翻多"
    return "觀望"

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    rows = get_sheet_data(SHEET_URL)
    for idx, row in enumerate(rows[1:], start=2):
        if not row[0]: continue
        chip = get_chip(row[0], today)
        note = generate_note(chip)
        update_sheet_note(SHEET_URL, idx, 4, note)
    print("備註更新完成")

if __name__ == "__main__":
    main()
