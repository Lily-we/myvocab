import os
import gspread
from google.oauth2.service_account import Credentials

from .models import Word

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def sync_words_from_sheets(
    spreadsheet: str = None,
    worksheet: str = None,
    creds_path: str = None,
) -> dict:
    """
    Pull rows from Google Sheets and upsert into Word model.
    Returns stats dict: {rows, upserted, skipped}
    """
    spreadsheet = spreadsheet or os.environ.get("SHEET_NAME", "RussianWords")
    worksheet = worksheet or os.environ.get("SHEET_TAB", "Sheet1")
    creds_path = creds_path or os.environ.get("GOOGLE_CREDS_PATH", "creds.json")

    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Creds file not found: {creds_path}. "
            f"Set GOOGLE_CREDS_PATH or place creds.json in project root."
        )

    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)

    ws = client.open(spreadsheet).worksheet(worksheet)
    rows = ws.get_all_records()

    upserted = 0
    skipped = 0

    for row in rows:
        # normalize headers just in case
        row = {str(k).strip().lower(): v for k, v in row.items()}

        w = (row.get("word") or "").strip()
        t = (row.get("translation") or "").strip()
        e = (row.get("example") or "").strip()

        if not w or not t:
            skipped += 1
            continue

        Word.objects.update_or_create(
            word=w,
            defaults={"translation": t, "example": e},
        )
        upserted += 1

    return {"rows": len(rows), "upserted": upserted, "skipped": skipped}
