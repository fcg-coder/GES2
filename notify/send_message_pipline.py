import requests
import sys

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python send_message.py <TOKEN> <CHAT_ID> <COMMIT_MESSAGE>")
        sys.exit(1)

    TOKEN = sys.argv[1]
    CHAT_ID = sys.argv[2]
    COMMIT_MESSAGE = sys.argv[3]
    send_message(TOKEN, CHAT_ID, COMMIT_MESSAGE)
