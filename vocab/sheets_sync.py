import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
from .models import Word

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def sync_words_from_sheets(spreadsheet_name: str = "RussianWords", worksheet_title: str | None = None) -> int:
    """
    Pull rows from Google Sheets and upsert into the Word table.
    Returns number of rows processed.
    """
    creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
    client = gspread.authorize(creds)

    sh = client.open(spreadsheet_name)
    ws = sh.worksheet(worksheet_title) if worksheet_title else sh.sheet1

    rows = ws.get_all_records()  # expects row1 headers
    for row in rows:
        word = (row.get("word") or "").strip()
        translation = (row.get("translation") or "").strip()
        example = (row.get("example") or "").strip()

        if not word or not translation:
            continue

        Word.objects.update_or_create(
            word=word,
            defaults={"translation": translation, "example": example},
        )

    return len(rows)
