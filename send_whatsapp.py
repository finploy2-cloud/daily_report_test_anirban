import requests
import json
import sys
import config


def send_message(to_number: str):
    """
    Send WhatsApp template message using Alots.io WhatsApp API
    """

    # ---------- VALIDATION ----------
    if not config.API_KEY:
        raise ValueError("API_KEY missing in config.py")

    if not config.SEND_MESSAGE_ENDPOINT_URL:
        raise ValueError("SEND_MESSAGE_ENDPOINT_URL missing in config.py")

    if not to_number.startswith("91") or not to_number.isdigit():
        raise ValueError("Phone number must be in international format. Example: 919876543210")

    # ---------- HEADERS ----------
    headers = {
        "X-API-KEY": config.API_KEY,
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json"
    }

    # ---------- PAYLOAD ----------
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,   # ✅ FIXED: use function argument
        "type": "template",
        "template": {
            "name": "test1",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": []
                }
            ]
        }
    }

    # ---------- DEBUG ----------
    print("\n--- SENDING PAYLOAD ---")
    print(json.dumps(payload, indent=2))

    # ---------- API CALL ----------
    try:
        url = config.SEND_MESSAGE_ENDPOINT_URL.replace("PhoneNumberID", config.PHONENUMBER_ID)
        print("Using URL:", url)
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("\n--- RESPONSE ---")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code in (200, 201):
            print("\n✅ Message accepted by API")
        else:
            print("\n❌ Message NOT accepted by API")

    except requests.exceptions.RequestException as e:
        print("\n❌ NETWORK / REQUEST ERROR")
        print(str(e))


# ---------- CLI ----------
if __name__ == "__main__":
    print("=== WhatsApp Template Sender ===")

    to = input("Enter recipient number (example: 919876543210): ").strip()

    if not to:
        print("❌ Invalid number")
        sys.exit(1)

    send_message(to)
