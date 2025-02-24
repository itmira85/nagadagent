import requests
import json
import telebot

# টেলিগ্রাম বট সেটআপ
BOT_TOKEN = "8190965782:AAGpSKPyMNRstdbp7zrZpLQ18vtTSRCs_3c"
bot = telebot.TeleBot(BOT_TOKEN)

# প্রথম রিকুয়েস্ট থেকে X-KM-REFRESH-TOKEN সংগ্রহ করা
def get_refresh_token():
    headers1 = {
        'Host': 'app2.mynagad.com:20002',
        'User-Agent': 'okhttp/3.14.9',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'X-KM-UserId': '60452556',
        'X-KM-User-AspId': '100012345612345',
        'X-KM-User-Agent': 'ANDROID/1164',
        'X-KM-DEVICE-FGP': '16D93CCB6CDF5B86D021AFF522BB4A4555CDEEE844E76F73FBF6B25B2EA09346',
        'X-KM-Accept-language': 'bn',
        'X-KM-AppCode': '01',
    }
    data1 = {
        "aspId": "100012345612345",
        "mpaId": None,
        "password": "B52B378CBEF9D95E5B93148CE26A9CAD0A6A39F79AD910697521EB9D2D58AB7A",
        "username": "01868690922"
    }
    response1 = requests.post("https://app2.mynagad.com:20002/api/login", headers=headers1, json=data1)
    if response1.status_code != 200:
        return None
    return response1.headers.get("X-KM-REFRESH-TOKEN")

# মোবাইল নাম্বার ইনপুট ও তথ্য অনুসন্ধান
def get_agent_info(mobile_no, refresh_token):
    headers2 = {
        'Host': 'app2.mynagad.com:20002',
        'User-Agent': 'okhttp/3.14.9',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'X-KM-UserId': '60452556',
        'X-KM-User-MpaId': '17379475106370043002311446537520',
        'X-KM-User-AspId': '100012345612345',
        'X-KM-User-Agent': 'ANDROID/1164',
        'X-KM-Accept-language': 'bn',
        'X-KM-AUTH-TOKEN': refresh_token,
        'X-KM-AppCode': '01',
    }
    data2 = {"mobileNo": mobile_no}
    response2 = requests.post("https://app2.mynagad.com:20002/api/external/agent/details", headers=headers2, json=data2)
    return response2.json() if response2.status_code == 200 else {"error": "Request failed"}

# ফরম্যাট করা রেসপন্স
def format_response(data):
    return (
        "♻️ INFO FOUND SUCCESS ♻️\n\n"
        f"👤 Name:- {data.get('name', 'N/A')}\n"
        f"🏢 Organization:- {data.get('orgName', 'N/A')}\n"
        f"🖼️ Photo URL:- {data.get('photoUrl', 'N/A')}\n"
        f"🆔 Merchant ID:- {data.get('merchantId', 'N/A')}\n"
        f"🏬 Bazar:- {data['address'].get('bazar', 'N/A')}\n"
        f"📍 Area:- {data['address'].get('area', 'N/A')}\n"
        f"🚔 Thana:- {data['address'].get('thana', 'N/A')}\n"
        f"🏙️ District:- {data['address'].get('district', 'N/A')}\n"
        f"🌍 Division:- {data['address'].get('division', 'N/A')}\n"
        f"📌 Latitude:- {data.get('latitude', 'N/A')}\n"
        f"📌 Longitude:- {data.get('longitude', 'N/A')}\n\n"
        "🛠️ Developer:- @I_am_Silent_b0y"
    )

# টেলিগ্রাম বট কমান্ড
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ℹ️ Nagad Agent Info জানতে মোবাইল নাম্বার দিন।")

@bot.message_handler(func=lambda message: message.text.lower() == "ℹ️ nagad agent info")
def ask_for_number(message):
    bot.reply_to(message, "আপনার নগদ এজেন্ট নাম্বার দিন।")
    bot.register_next_step_handler(message, process_number)

# মোবাইল নাম্বার প্রসেসিং
def process_number(message):
    mobile_no = message.text.strip()
    if not mobile_no.startswith("01") or not mobile_no.isdigit() or len(mobile_no) != 11:
        bot.reply_to(message, "❌ ভুল নাম্বার! দয়া করে সঠিক ফরম্যাটে দিন।")
        return
    refresh_token = get_refresh_token()
    if not refresh_token:
        bot.reply_to(message, "❌ X-KM-REFRESH-TOKEN পাওয়া যায়নি।")
        return
    response_data = get_agent_info(mobile_no, refresh_token)
    formatted_message = format_response(response_data)
    bot.reply_to(message, formatted_message)

# বট চালু করা
bot.polling(none_stop=True)