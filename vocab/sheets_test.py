import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)

sheet = client.open("RussianWords").sheet1
rows = sheet.get_all_records()

print(rows)
