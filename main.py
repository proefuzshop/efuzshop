import telebot
from telebot import types
from flask import Flask
import threading
import os
import json
import html

# --- SERVER (Bot o'chib qolmasligi uchun) ---
app = Flask('')
@app.route('/')
def home(): return "EFUZ TIME SHOP Faol! 🚀"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- SOZLAMALAR ---
TOKEN = "8298795746:AAGkZaREbwwpRijHC4N8UgfUMGYQ7_T2jlc"
ADMIN_ID = 8144030372
CHANNEL_ID = "@PRO_EFUZ_SHOP"
bot = telebot.TeleBot(TOKEN)

# Siz yuborgan rasmlar
OLISH_IMAGE = "https://i.ibb.co/3ykC6W2/olaman-efuz.jpg" 
USER_DB = "users_pro.json"
ADS_DB = "published_ads.json"

# --- BAZA FUNKSIYALARI ---
def save_user(user_id):
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f: json.dump([], f)
    with open(USER_DB, "r") as f: users = json.load(f)
    if str(user_id) not in users:
        users.append(str(user_id))
        with open(USER_DB, "w") as f: json.dump(users, f)

def get_ads():
    if not os.path.exists(ADS_DB): return {}
    with open(ADS_DB, "r") as f: return json.load(f)

def save_ad(uid, ad_data):
    ads = get_ads()
    if str(uid) not in ads: ads[str(uid)] = []
    ads[str(uid)].append(ad_data)
    with open(ADS_DB, "w") as f: json.dump(ads, f)

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
    return markup

# --- KOMANDALAR ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"👋 <b>Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        f"<b>EFUZ TIME SHOP</b> botiga xush kelibsiz! 😊\n"
        f"Bu yerda siz o'z eFootball akkauntlaringizni tez va xavfsiz soting yoki o'zingizga mosini toping.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "📚 Qoidalar")
def rules(message):
    text = (
        "🛑 <b>BOTDAN FOYDALANISH QOIDALARI:</b>\n\n"
        "1. Faqat <b>eFootball</b> akkauntlari reklamasi ruxsat etiladi.\n"
        "2. Narxni asossiz pasaytirish yoki yolg'on ma'lumot berish taqiqlanadi.\n"
        "3. Qoidalarni buzgan foydalanuvchi <b>MUDDATSIZ</b> bloklanadi.\n\n"
        "⚠️ <i>E'loningiz o'chib ketmasligi uchun qoidalarga amal qiling!</i>"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "💰 Elon narxlari")
def prices(message):
    text = (
        "🎉 <b>ZO'R YANGILIK!</b>\n\n"
        "Hozirda botimizda <b>AKSIYA</b> ketmoqda. E'lon berish barcha uchun <b>MUTLAQO BEPUL!</b> 🎁\n\n"
        "Fursatdan foydalanib, e'loningizni hoziroq kanalga joylang!"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def show_admins(message):
    text = "♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n\nFaqatgina ushbu adminlarga kanal nomidan javob beriladi. Ehtiyot bo'ling!"
    bot.send_message(message.chat.id, text, reply_markup=admin_buttons(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🔍 Akkaunt qidirish")
def search_off(message):
    bot.send_message(message.chat.id, "❌ <b>Kechirasiz, qidiruv tizimi vaqtincha o'chirilgan!</b>", parse_mode="HTML")

# --- ELON BERISH ---
@bot.message_handler(func=lambda m: m.text == "➕ Elon berish")
def ask_type(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔺 Sotish eloni", callback_data="type_sotish"),
        types.InlineKeyboardButton("🔻 Olish eloni", callback_data="type_olish")
    )
    bot.send_message(message.chat.id, "❓ <b>Qanday turdagi e'lon joylamoqchisiz?</b>\n\nTanlang:", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def handle_type(call):
    ad_type = call.data.split("_")[1]
    user_temp[call.message.chat.id] = {"type": ad_type}
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    if ad_type == "sotish":
        msg = bot.send_message(call.message.chat.id, "📸 <b>Akkauntingizning rasmini yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, s_photo)
    else:
        msg = bot.send_message(call.message.chat.id, "💵 <b>Budjetingizni kiriting:</b>\n(Masalan: 500.000)", parse_mode="HTML")
        bot.register_next_step_handler(msg, o_budget)

# --- SOTISH BOSQICHLARI ---
def s_photo(message):
    if not message.photo:
        msg = bot.send_message(message.chat.id, "⚠️ Iltimos, faqat rasm yuboring!")
        bot.register_next_step_handler(msg, s_photo); return
    user_temp[message.chat.id]['photo'] = message.photo[-1].file_id
    msg = bot.send_message(message.chat.id, "💰 <b>Akkaunt narxini yozing:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, s_price)

def s_price(message):
    user_temp[message.chat.id]['price'] = message.text
    msg = bot.send_message(message.chat.id, "🔄 <b>Obmen bormi? (Bor/Yo'q):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, s_obmen)

def s_obmen(message):
    user_temp[message.chat.id]['obmen'] = message.text
    msg = bot.send_message(message.chat.id, "⚠️ <b>Akkaunt holati (Toza/Bandi):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, s_info)

def s_info(message):
    user_temp[message.chat.id]['info'] = message.text
    msg = bot.send_message(message.chat.id, "📝 <b>Batafsil ma'lumot (Masalan: Son blitz 102):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, s_final)

def s_final(message):
    uid = message.chat.id
    d = user_temp[uid]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    
    caption = (
        f"<b>#SOTILADI</b>\n\n"
        f"💵 <b>Narx:</b> {d['price']} so'm\n"
        f"♻️ <b>Obmen ko'rish:</b> {d['obmen']}\n"
        f"⚠️ <b>Google & Game Center:</b> {d['info']}\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"📋 <b>Qo'shilgan ma'lumot:</b>\n<i>{message.text}</i>\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"◾️ @eFadmin_uz\n◾️ @eFGarant\n◾️ @CR7_ISLAM07\n"
        f"◾️ @KAMOLXUJA19\n◾️ @Sarik_CR7\n◾️ @eF_Rasulov\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n@{bot.get_me().username}"
    )
    sent = bot.send_photo(CHANNEL_ID, d['photo'], caption=caption, parse_mode="HTML")
    
    ad_save = {'photo': d['photo'], 'caption': caption, 'fast': 2, 'mid': sent.message_id}
    save_ad(uid, ad_save)
    bot.send_message(uid, "🎉 <b>Tabriklaymiz!</b> E'loningiz kanalga joylandi.", reply_markup=main_menu(), parse_mode="HTML")

# --- OLISH BOSQICHLARI ---
def o_budget(message):
    user_temp[message.chat.id]['budget'] = message.text
    msg = bot.send_message(message.chat.id, "📋 <b>Qanday akkaunt kerak? (To'liq ma'lumot bering):</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, o_final)

def o_final(message):
    uid = message.chat.id
    budget = user_temp[uid]['budget']
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    
    caption = (
        f"<b>#OLINADI #FAQAT_TOZA</b>\n\n"
        f"💵 <b>BUDJET:</b> {budget} so'm\n"
        f"📋 <b>Ma'lumot:</b>\n<i>{message.text}</i>\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"◾️ @eFadmin_uz\n◾️ @eFGarant\n◾️ @CR7_ISLAM07\n"
        f"◾️ @KAMOLXUJA19\n◾️ @Sarik_CR7\n◾️ @eF_Rasulov\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n@{bot.get_me().username}"
    )
    bot.send_photo(CHANNEL_ID, OLISH_IMAGE, caption=caption, parse_mode="HTML")
    bot.send_message(uid, "✅ <b>Sizning qidiruv e'loningiz yuborildi!</b>", reply_markup=main_menu(), parse_mode="HTML")

# --- ELONLARIM VA FAST ---
@bot.message_handler(func=lambda m: m.text == "📂 Elonlarim")
def my_ads(message):
    uid = str(message.chat.id)
    ads = get_ads()
    if uid in ads and ads[uid]:
        for idx, ad in enumerate(ads[uid]):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f"⚡️ FAST ({ad['fast']})", callback_data=f"fast_{idx}"))
            bot.send_photo(message.chat.id, ad['photo'], caption=ad['caption'], reply_markup=markup, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "😔 <b>Sizda hali e'lonlar mavjud emas.</b>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("fast_"))
def handle_fast(call):
    idx = int(call.data.split("_")[1])
    uid = str(call.message.chat.id)
    ads = get_ads()
    
    if ads[uid][idx]['fast'] > 0:
        ads[uid][idx]['fast'] -= 1
        with open(ADS_DB, "w") as f: json.dump(ads, f)
        
        bot.send_message(CHANNEL_ID, "⚡️ <b>#TEZKOR_SOTUV</b>\n\nUshbu e'lon egasi shoshilinch sotmoqda!", reply_to_message_id=ads[uid][idx]['mid'])
        bot.answer_callback_query(call.id, "✅ E'loningiz kanal tepasiga ko'tarildi!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ FAST imkoniyati tugagan!", show_alert=True)

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
    
