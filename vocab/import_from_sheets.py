import gspread
from google.oauth2.service_account import Credentials
from vocab.models import Word

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def main():
    creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
    client = gspread.authorize(creds)

    ws = client.open("RussianWords").sheet1
    rows = ws.get_all_records()

    print("rows:", len(rows))
    if rows:
        print("keys:", list(rows[0].keys()))
        print("row0:", rows[0])

    upserted = 0
    for row in rows:
        # normalize keys just in case
        row = {str(k).strip().lower(): v for k, v in row.items()}

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

main()
