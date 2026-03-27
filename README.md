# Finploy Daily WhatsApp Reports System

## Executive Summary
This project automates the delivery of daily performance reports for the recruitment team. It synchronizes data from Google Sheets, calculates key performance indicators (KPIs) for each recruiter, and delivers formatted reports directly to their WhatsApp via the 1automations (Meta Cloud API) platform.

---

## 🛠 Technical Architecture

### 1. Data Source (Google Sheets)
- **Sheet Name**: `Tracker -Candidates`
- **Tab**: `LINEUP`
- **Authentication**: Integrated via Google Service Account (Hardcoded IAM credentials within the script for CI/CD compatibility).

### 2. Messaging Engine (WhatsApp)
- **Provider**: 1automations (Enterprise Dashboard for Meta Cloud API).
- **Endpoint**: `https://crmapi.1automations.com/api/meta`
- **Message Format**: WhatsApp Template `finploy_daily_report_5`.
- **Payload**: Dynamic 10-field template including conversion rates, interview counts, and gap analysis.

### 3. Deployment & Automation
- **Platform**: GitHub Actions.
- **Schedule**: 
    - 06:00 AM IST (Daily)
    - 06:00 PM IST (Daily)
- **Environment**: Ubuntu Linux runner using Python 3.10.

---

## 📋 KPIs Tracked
The system automatically calculates the following metrics per recruiter:
1. **Conversion**: Lineup vs. Rejected counts.
2. **Pipeline**: Current candidate statuses.
3. **Outcome**: Shortlisted, Selected, and Joined counts.
4. **Schedule**: Interview counts for Today, Tomorrow, and Day After.
5. **Efficiency**: Candidate gap, client gap, and remark gap analysis.
6. **Follow-ups**: Pending feedback from clients.

---

## ⚙️ Configuration & Secrets

For security, the system uses **GitHub Repository Secrets** to manage API credentials. The following secrets must be maintained:

| Secret Name | Description |
| ----------- | ----------- |
| `WHATSAPP_ACCESS_TOKEN` | Permanent/Temporary Bearer Token from 1automations dashboard. |
| `WHATSAPP_PHONE_NUMBER_ID` | Business Phone Number ID provided by Meta/1automations. |
| `WHATSAPP_API_VERSION` | Default: `v21.0` |
| `WHATSAPP_BASE_URL` | Endpoint: `https://crmapi.1automations.com/api/meta` |

---

## 🚀 Setup Instructions

### Local Development
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file with the secrets mentioned above.
4. Run: `python single_script.py`.

### Production (GitHub)
The bot runs automatically on the set schedule. To trigger a report manually:
1. Navigate to the **Actions** tab in GitHub.
2. Select **Finploy Daily WhatsApp Reports**.
3. Click **Run workflow**.

---

## ⚠️ Maintenance Note
- **Google Credentials**: IAM credentials are hardcoded in `single_script.py` under `SERVICE_ACCOUNT_INFO`. If the service account is rotated, update this dictionary.
- **Template Changes**: If the WhatsApp template `finploy_daily_report_5` is modified in the dashboard, ensure the `fields` list in the Python script is updated to match the new field count.
