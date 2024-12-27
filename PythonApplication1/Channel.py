import requests

BOT_TOKEN = "7611733325:AAGZR_DWPeXzR9axBgzMT-qZO37NCpeH34o"

CHANNEL_ID = "sigmasignals2004"

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=@{CHANNEL_ID}&text={text}"
    response = requests.post(url)
    if response.status_code == 200:
        print("Success")
    else:
        print(f"Error: {response.status_code}, {response.text}")


