import requests

BOT_TOKEN = "7995798682:AAGhVu4qVodVt5bhEGrN_xsiDjYKDxUVHc4"

CHANNEL_ID = "flashsignals0013"

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=@{CHANNEL_ID}&text={text}"
    response = requests.post(url)
    if response.status_code == 200:
        print("Success")
    else:
        print(f"Error: {response.status_code}, {response.text}")


