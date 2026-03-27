import pandas as pd
import gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ====================================================
# GOOGLE SHEET CONFIG
# ====================================================
SPREADSHEET_NAME = "Tracker -Candidates"
SHEET_TAB = "LINEUP"

RECRUITERS = ["Soham", "Shraddha", "Nandhini", "Antara"]

STATUS_LIST = [
    "Lineup", "unpaid",
    "Scheduled interview",
    "Call back at lineup stage",
    "Switchoff at lineup stage",
    "Rejected", "Shortlisted",
    "Interview done",
    "joined", "Joining", "Selected", "Joined",
    "Status",
    "Going for interview",
    "Chasing for client's feedback"
]

# ====================================================
# WHATSAPP (NEW PANEL) CONFIG
# ====================================================
# Use 'or' to fall back to defaults if environment variables are empty strings
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
API_VERSION = os.getenv("WHATSAPP_API_VERSION") or "v21.0"
BASE_URL = os.getenv("WHATSAPP_BASE_URL") or "https://crmapi.1automations.com/api/meta"

TEMPLATE_NAME = "finploy_daily_report_5"

if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
    API_URL = None
    print("⚠️ WARNING: WHATSAPP_ACCESS_TOKEN or WHATSAPP_PHONE_NUMBER_ID is missing!")
else:
    API_URL = f"{BASE_URL}/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

# ====================================================
# PHONE NUMBERS
# ====================================================
RECRUITER_NUMBERS = {
    "Anirban": "9082658097"
}

ADMIN_NUMBERS = [
    "918104468345",
    "918104748399",
    "919324399045"
]

# ====================================================
# GOOGLE AUTH (HARDCODED)
# ====================================================
SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "manual-automation",
  "private_key_id": "63af68d9de247904c255d94aee84f6c957029ed7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDCVVy75Z9xPgUm\nff9lCmRQrh1dH9pOhehbgQm+xOzFTMrJ24RQtbopBk0l6hXvENe7UmvUybw2XaiT\nZWHUNi/SmOXQPsGlSEO5MTGEMO7uYnwtX9iAWaWXv8yZkCbrtUBdobyHVuOIwXU1\nU8nC6NYL+lOpjtX2b87tAhCx7oEuRqYxnufnp7pBf6SpKg8UlWBqga8aPwDxNMjK\nwML1cd94TG5i5N/9VOFJyE9sy1KiZXAN29cuFbGpvIFCfGI2MYvansLBYvVSg/cz\ngA4zPy2H9A4UdwfhCn07yJuoa3OpkWJAWDQhSG80gumWwP38+jqhjEj8dt18oqBX\nEVRmCSpXAgMBAAECggEAENhXEv8rAc/B9jMKyIaM6S9xN9Qd13D6Z2Aj6PI8oeJF\nBm1YUVSx/9deKEYGbl7JNyFvBmwRkVbaA3jQxj/c3QZIOXO508AUBWwIYkXe7Yas\n7pP1z4kLIRXM6uzDaurJsF682bBu8GObQNWep3NeW9Ma8xeAtX1onu5vEGAKY5Pb\ny78JCvbmKKtjPvRVZseflBAJ6crSPgvGUT/jKTzWzNxN66pViPlDAD5FrffGE8jF\ntoegkn6eF/ogleqQqPem+1arqxIy4VOVDaGLhUFm3Lfu/Pcb3qUxh+vjcpnP0Yu8\nO9BUOicDzoYEhjwJpDt9Cy1BCc95Uy2YzTrehSySBQKBgQDqvSLYYrchghp8IaiA\n3354DQtIR163c9sad+dg90pbcT3c7qcuqKm+JFJHdJgRs8FSEA0YLMBPw1FOFTr/\nbOpCoiegtCm85NAbatGhw/vR2mGQgiWQ8IsiZYHE+VVEbPq1u7tAtoyQaP6Sz0Gb\nsPTSquVdz0se0s9VUAIoz1lgAwKBgQDT71nnfNS6BjA0Y2JD4nD7SoAZViyKfh+G\nVf6QgCImxDrl9xCVEcIF+YyRBx5RyI+51L04HcCyqklBq5uIWHCLUnPrDEK5PBqh\nyOE0IunbKHpbZxj/5FW867VLwK/51cAikWaf5Fml5nNTQq098sYd11G7GRRSDYCl\nnwOlKzhuHQKBgQC5jcqmm9nBHhQLfZuyS3iwMzdw6iHACE/xK0j2SGQ5xlktdGUp\nJ+AN0q5Ll6nBjINLeC6xpmZaZr21aGjbkd/XzlBe4yt/CqxKj/Sn18EOUH8A+S/y\n04JYLT8YUjOJxE+mKoDJlcOlP6nEqRpmlMniYX6v2fW6ps+H05fxZH50uwKBgQC2\ndJg8z15AbHVxlKITeU31OTVBGswrytsPBteqxXUhVMy0EFipTWlxRV77uFok5Hq/\n7GOefRbZefqpW7kBz8nMWAbNs3d6C0GOSOeAwBH+iEGWkRKXspcRlwc0mUWm25uW\n5wCn5Ko9RkHAy2VkMK7ZH/cQEU5KOa+oZlZ4CtaBDQKBgQCNkd79rRxDIeK9Kr8/\n6Uf0q7Op+HdgB41dxgVVdB8HltbWZoA8SPHHQcImUNpF2QaqSHV+hF12V97JJ6tv\nmYnADfOythlFmjKTX8mM9S/CRdwgOBCRZ5FCYNpXnK0yavlsubsICuYHEcosffYT\n1omFurdvmRyw2Wb7EpGsE4Ps1A==\n-----END PRIVATE KEY-----\n",
  "client_email": "harsh-manual-automation@manual-automation.iam.gserviceaccount.com",
  "client_id": "104274696189537153996",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/harsh-manual-automation%40manual-automation.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    SERVICE_ACCOUNT_INFO, scope
)
client = gspread.authorize(creds)

sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_TAB)
df = pd.DataFrame(sheet.get_all_records())
print("✅ Google Sheet Loaded")

# ====================================================
# WHATSAPP SAFE VALUE
# ====================================================
def wa_safe(value):
    if value is None:
        return "0"
    if isinstance(value, float) and pd.isna(value):
        return "0"
    v = str(value).strip()
    return v if v != "" else "0"

# ====================================================
# HELPERS
# ====================================================
def safe_count(row, key):
    return int(row[key]) if key in row.index else 0

def count_interviews_on_date(df_rec, date_str):
    if "Interview Date" not in df_rec.columns:
        return 0
    sub = df_rec[df_rec["Interview Date"].notna()]
    return int((sub["Interview Date"].dt.strftime("%Y-%m-%d") == date_str).sum())

def calculate_gap_buckets(df_rec, col):
    if col not in df_rec.columns:
        return 0, 0, 0
    s = pd.to_numeric(df_rec[col], errors="coerce").dropna()
    return (
        int(s[(s >= 1) & (s <= 2)].count()),
        int(s[(s >= 3) & (s <= 5)].count()),
        int(s[s > 5].count()),
    )

# ====================================================
# SEND WHATSAPP (FINAL – WATIFLY COMPLIANT)
# ====================================================
def send_whatsapp_message(number, fields):

    if not number or len(number) != 12 or not number.isdigit():
        print(f"❌ INVALID PHONE SKIPPED: {number}")
        return

    if len(fields) != 10:
        print(f"❌ BLOCKED (invalid field count): {number}")
        return

    if any(v in ["", "nan", "None"] for v in fields):
        print(f"❌ BLOCKED (empty value): {number}")
        print(fields)
        return

    if not API_URL:
        # Warning already printed once at the top of the script
        return

    # Meta API uses 'to' without the '+' prefix, which matches your 12-digit format (91...)
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "template",
        "template": {
            "name": TEMPLATE_NAME,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": str(f)} for f in fields]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=20)
        resp = r.json() if "application/json" in r.headers.get("Content-Type", "") else r.text
        print(f"➡ {number} | {r.status_code} | {resp}")
    except Exception as e:
        print(f"⚠️ WhatsApp API Error for {number}: {e}")

# ====================================================
# MAIN LOGIC
# ====================================================
df["Recruiter"] = df["Recruiter"].astype(str).str.strip().str.title()
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
df["Interview Date"] = pd.to_datetime(df["Interview Date"], format="%d-%m-%Y", errors="coerce")

df = df[df["Status"].isin(STATUS_LIST)]
df = df[df["Recruiter"].isin(RECRUITERS)]

grouped = df.groupby(["Recruiter", "Status"]).size().unstack(fill_value=0)

today = datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
day_after = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

print("🚀 Sending Reports")

payloads = {}

for rec in RECRUITERS:
    if rec not in grouped.index:
        continue

    row = grouped.loc[rec]
    df_rec = df[df["Recruiter"] == rec]

    fields = [
        wa_safe(rec),
        wa_safe(f"{safe_count(row,'Lineup')} | {safe_count(row,'Rejected')}"),
        wa_safe(safe_count(row,"Status")),
        wa_safe(f"{safe_count(row,'Shortlisted')} | {safe_count(row,'Selected')} | {safe_count(row,'Joining')} | {safe_count(row,'Joined')}"),
        wa_safe(f"{count_interviews_on_date(df_rec,today)} | {count_interviews_on_date(df_rec,tomorrow)} | {count_interviews_on_date(df_rec,day_after)}"),
        wa_safe(f"{safe_count(row,'Interview done')} | {safe_count(row,'Going for interview')}"),
        wa_safe(" | ".join(map(str, calculate_gap_buckets(df_rec,"candidate_gap")))),
        wa_safe(" | ".join(map(str, calculate_gap_buckets(df_rec,"client_gap")))),
        wa_safe(" | ".join(map(str, calculate_gap_buckets(df_rec,"Remark_gap")))),
        wa_safe(safe_count(row, "Chasing for client's feedback")),
    ]

    payloads[rec] = fields
    send_whatsapp_message(RECRUITER_NUMBERS[rec], fields)

for admin in ADMIN_NUMBERS:
    for rec in payloads:
        send_whatsapp_message(admin, payloads[rec])

print("✅ DONE")
