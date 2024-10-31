import requests
import sys

def send_message(token, chat_id, commit_message, comments):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    # Формируем сообщение
    message = f"🤖👨‍💻\nNew commit: {commit_message}"
    if comments:
        message += f"\nDescription: {comments}"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Если хотите использовать HTML для форматирования
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python send_message.py <TOKEN> <CHAT_ID> <COMMIT_MESSAGE> <COMMENTS>")
        sys.exit(1)

    TOKEN = sys.argv[1]
    CHAT_ID = sys.argv[2]
    COMMIT_MESSAGE = sys.argv[3]
    COMMENTS = sys.argv[4]
    
    result = send_message(TOKEN, CHAT_ID, COMMIT_MESSAGE, COMMENTS)
    if result and result.get("ok"):
        print("Message sent successfully!")
    else:
        print("Failed to send message.")
