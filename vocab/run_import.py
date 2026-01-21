import gspread
from google.oauth2.service_account import Credentials
from vocab.models import Word

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)

ws = client.open("RussianWords").sheet1
rows = ws.get_all_records()

print("Rows from sheet:", len(rows))
print("Example row:", rows[0] if rows else None)

upserted = 0
for row in rows:
    w = (row.get("word") or "").strip()
    t = (row.get("translation") or "").strip()
    e = (row.get("example") or "").strip()

    if not w or not t:
        continue

    Word.objects.update_or_create(
        word=w,
        defaults={"translation": t, "example": e},
    )
    upserted += 1

print("Upserted:", upserted)
print("DB count now:", Word.objects.count())

