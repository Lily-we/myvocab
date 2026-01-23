import os

import gspread
from django.core.management.base import BaseCommand
from google.oauth2.service_account import Credentials

from vocab.models import Word

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class Command(BaseCommand):
    help = "Sync words from Google Sheets into the Word model (upsert by word)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--spreadsheet",
            default=os.environ.get("SHEET_NAME", "RussianWords"),
            help="Google Spreadsheet title (default: RussianWords or env SHEET_NAME)",
        )
        parser.add_argument(
            "--worksheet",
            default=os.environ.get("SHEET_TAB", "Sheet1"),
            help="Worksheet/tab name (default: Sheet1 or env SHEET_TAB)",
        )
        parser.add_argument(
            "--creds",
            default=os.environ.get("GOOGLE_CREDS_PATH", "creds.json"),
            help="Path to service account creds JSON (default: creds.json or env GOOGLE_CREDS_PATH)",
        )

    def handle(self, *args, **options):
        spreadsheet = options["spreadsheet"]
        worksheet = options["worksheet"]
        creds_path = options["creds"]

        if not os.path.exists(creds_path):
            self.stderr.write(self.style.ERROR(f"Creds file not found: {creds_path}"))
            self.stderr.write(
                "Tip: set GOOGLE_CREDS_PATH env var in production (Render Secret File)."
            )
            return

        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        client = gspread.authorize(creds)

        ws = client.open(spreadsheet).worksheet(worksheet)
        rows = ws.get_all_records()

        self.stdout.write(f"Rows from sheet: {len(rows)}")
        if rows:
            self.stdout.write(f"Headers: {list(rows[0].keys())}")

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

        self.stdout.write(self.style.SUCCESS(f"Upserted: {upserted}"))
        self.stdout.write(f"Skipped: {skipped}")
        self.stdout.write(f"DB count now: {Word.objects.count()}")
