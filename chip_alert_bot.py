import os, requests, datetime
from auth_google import get_sheet_data

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_URL = os.getenv("SHEET_URL")

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    stocks = get_sheet_data(SHEET_URL)
    messages = []
    for row in stocks[1:]:
        if len(row) >= 3 and row[2].lower() == "on":
            note = row[3] if len(row) > 3 else ""
            messages.append(f"{row[0]} {row[1]} {note}")

    if messages:
        msg = f"[{today}] 籌碼啟動\n" + "\n".join(messages)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': msg}
        res = requests.post(url, data=data)
        print("推播完成", res.status_code)

if __name__ == "__main__":
    main()
