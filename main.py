import telebot
from telebot import types
from flask import Flask
import threading
import os
import json
import html

# --- SERVER (Uyg'oq tutish uchun) ---
app = Flask('')
@app.route('/')
def home(): return "EFUZ TIME SHOP Active! 🌟"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- SOZLAMALAR ---
TOKEN = "8298795746:AAGkZaREbwwpRijHC4N8UgfUMGYQ7_T2jlc"
ADMIN_ID = 8144030372
CHANNEL_ID = "@PRO_EFUZ_SHOP"
bot = telebot.TeleBot(TOKEN)

USER_DB = "users_pro.json"
# Siz yuborgan "Akkaunt Olaman" rasmining havolasi
OLISH_IMAGE = "https://i.ibb.co/3ykC6W2/olaman-efuz.jpg" 

# --- BAZA FUNKSIYALARI ---
def save_user(user_id):
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f: json.dump([], f)
    with open(USER_DB, "r") as f: users = json.load(f)
    if str(user_id) not in users:
        users.append(str(user_id))
        with open(USER_DB, "w") as f: json.dump(users, f)

def get_users():
    if not os.path.exists(USER_DB): return []
    with open(USER_DB, "r") as f: return json.load(f)

user_temp = {}

# --- KLAVIATURALAR ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🔍 Akkaunt qidirish"))
    markup.add(types.KeyboardButton("➕ Elon berish"), types.KeyboardButton("📂 Elonlarim"))
    markup.add(types.KeyboardButton("👨‍💻 Adminlar"), types.KeyboardButton("📚 Qoidalar"))
    markup.add(types.KeyboardButton("💰 Elon narxlari"))
    return markup

def admin_buttons():
    markup = types.InlineKeyboardMarkup(row_width=2)
    admins = [
        ("💂‍♂️ @eFadmin_uz", "https://t.me/eFadmin_uz"),
        ("💂‍♂️ @eFGarant", "https://t.me/eFGarant"),
        ("💂‍♂️ @CR7_ISLAM07", "https://t.me/CR7_ISLAM07"),
        ("💂‍♂️ @KAMOLXUJA19", "https://t.me/KAMOLXUJA19"),
        ("💂‍♂️ @Sarik_CR7", "https://t.me/Sarik_CR7"),
        ("💂‍♂️ @Cosmos19", "https://t.me/Cosmos19"),
        ("💂‍♂️ @eF_Rasulov", "https://t.me/eF_Rasulov")
    ]
    for name, url in admins:
        markup.add(types.InlineKeyboardButton(text=name, url=url))
    markup.add(types.InlineKeyboardButton("👨‍💻 Dasturchi", url="https://t.me/davlatbekturgunboyev"))
    return markup

# --- KOMANDALAR ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"👋 <b>Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        f"<b>EFUZ TIME SHOP</b> botiga xush kelibsiz. Bu yerda siz xavfsiz va tezkor e'lon berishingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "📚 Qoidalar")
def rules(message):
    text = (
        "<b>Ushbu botdan faqat efootball akkaunt reklamasi uchun foydalaning.</b>\n\n"
        "⚠️ Boshqa har qanday maqsadda foydalansangiz yoki akkaunt narxini tushirib "
        "e'lon bersangiz, e'loningiz o'chirib yuboriladi, butunlay blok bo'lasiz va pulingiz qaytarilmaydi!"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def show_admins(message):
    text = (
        "♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        "◾️ @eFadmin_uz\n◾️ @eFGarant\n◾️ @CR7_ISLAM07\n"
        "◾️ @KAMOLXUJA19\n◾️ @Sarik_CR7\n◾️ @eF_Rasulov\n\n"
        "Faqatgina ushbu adminlarga kanal nomidan javob beriladi."
    )
    bot.send_message(message.chat.id, text, reply_markup=admin_buttons(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "💰 Elon narxlari")
def prices(message):
    text = (
        "🛍 <b>Akkauntlarga e'lon berish narxlari:</b>\n\n"
        "0 dan 250 000 gacha — 4 000 so'm\n"
        "250 001 dan 750 000 gacha — 8 000 so'm\n"
        "750 001 dan 1 000 000 gacha — 10 000 so'm\n"
        "1 000 001 dan 2 000 000 gacha — 12 000 so'm\n"
        "2 000 001 dan 10 000 000 gacha — 15 000 so'm\n\n"
        "♻️ <b>Botda avto to'lov qilish imkoniyati mavjud!</b>\n\n"
        "❗ Akkaunt olaman deb reklama berishingiz ham mumkin!"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🔍 Akkaunt qidirish")
def search_off(message):
    bot.send_message(message.chat.id, "❌ <b>Qidiruv tizimi o'chirilgan!</b>", parse_mode="HTML")

# --- ELON BERISH ---
@bot.message_handler(func=lambda m: m.text == "➕ Elon berish")
def start_ad(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔺 Sotish eloni", callback_data="type_sotish"),
        types.InlineKeyboardButton("🔻 Olish eloni", callback_data="type_olish")
    )
    bot.send_message(
        message.chat.id, 
        "❓ <b>Qanday turdagi elon joylamoqchisiz?</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def choose_type(call):
    ad_type = call.data.split("_")[1]
    user_temp[call.message.chat.id] = {"type": ad_type}
    if ad_type == "sotish":
        msg = bot.send_message(call.message.chat.id, "📸 <b>Akkaunt rasmini yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_photo)
    else:
        msg = bot.send_message(call.message.chat.id, "💵 <b>Elon uchun budjetingizni yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_budget)

# SOTISH BOSQICHLARI
def process_photo(message):
    if not message.photo:
        bot.register_next_step_handler(message, process_photo); return
    user_temp[message.chat.id]['photo'] = message.photo[-1].file_id
    msg = bot.send_message(message.chat.id, "💰 <b>Narxini kiriting:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_price)

def process_price(message):
    user_temp[message.chat.id]['price'] = message.text
    msg = bot.send_message(message.chat.id, "🔄 <b>Obmen bormi?:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_obmen)

def process_obmen(message):
    user_temp[message.chat.id]['obmen'] = message.text
    msg = bot.send_message(message.chat.id, "⚠️ <b>Holati (Toza/Bandi):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_info)

def process_info(message):
    user_temp[message.chat.id]['info'] = message.text
    msg = bot.send_message(message.chat.id, "📋 <b>Qo'shimcha ma'lumot:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, finish_sotish)

def finish_sotish(message):
    data = user_temp[message.chat.id]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.chat.id}"
    caption = (
        f"<b>#SOTILADI</b>\n\n"
        f"💵 <b>Narx:</b> {data['price']} so'm\n"
        f"♻️ <b>Obmen ko'rish:</b> {data['obmen']}\n"
        f"⚠️ <b>Google & Game Center:</b> {data['info']}\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"📋 <b>Qo'shilgan ma'lumot:</b>\n<i>{message.text}</i>\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"◾️ @eFadmin_uz\n◾️ @eFGarant\n◾️ @CR7_ISLAM07\n"
        f"◾️ @KAMOLXUJA19\n◾️ @Sarik_CR7\n◾️ @eF_Rasulov\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n@{bot.get_me().username}"
    )
    bot.send_photo(CHANNEL_ID, data['photo'], caption=caption, parse_mode="HTML")
    bot.send_message(message.chat.id, "✅ E'lon kanalga yuborildi!", reply_markup=main_menu())

# OLISH BOSQICHLARI
def process_budget(message):
    user_temp[message.chat.id]['budget'] = message.text
    msg = bot.send_message(message.chat.id, "📋 <b>Qanday akkaunt kerakligini to'liq yozing:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, finish_olish)

def finish_olish(message):
    data = user_temp[message.chat.id]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.chat.id}"
    caption = (
        f"<b>#OLINADI #FAQAT_TOZA</b>\n\n"
        f"💵 <b>BUDJET:</b> {data['budget']} so'm\n"
        f"📋 <b>Ma'lumot:</b>\n<i>{message.text}</i>\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"◾️ @eFadmin_uz\n◾️ @eFGarant\n◾️ @CR7_ISLAM07\n"
        f"◾️ @KAMOLXUJA19\n◾️ @Sarik_CR7\n◾️ @eF_Rasulov\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n@{bot.get_me().username}"
    )
    bot.send_photo(CHANNEL_ID, OLISH_IMAGE, caption=caption, parse_mode="HTML")
    bot.send_message(message.chat.id, "✅ Olish e'loningiz yuborildi!", reply_markup=main_menu())
    del user_temp[message.chat.id]

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
    
