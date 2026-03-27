import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ====================================================
# GOOGLE AUTH (FILE BASED, SAFE)
# ====================================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "google_key.json",
    scope
)

client = gspread.authorize(creds)

# ====================================================
# SIMPLE TEST: OPEN SHEET
# ====================================================
SPREADSHEET_NAME = "Tracker -Candidates"
SHEET_TAB = "LINEUP"

sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_TAB)
rows = sheet.get_all_records()

print("✅ AUTH SUCCESSFUL")
print(f"✅ Rows fetched: {len(rows)}")
