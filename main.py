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
def home(): return "PRO EFUZ SHOP boti faol! 🌟"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- SOZLAMALAR ---
TOKEN = "8298795746:AAGkZaREbwwpRijHC4N8UgfUMGYQ7_T2jlc"
ADMIN_ID = 8144030372
CHANNEL_ID = "@PRO_EFUZ_SHOP"
bot = telebot.TeleBot(TOKEN)

# Siz yuborgan asl garantlar ro'yxati (Hech qanday o'zgarishsiz)
GARANTLAR = "@davlatbekturgunboyev, @shoniyozov_12, @Giyosov_o22, @ERKINOV277, @OTABEK_LM_10, @Utop41"

# Olish eloni uchun siz tanlagan rasm
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
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔍 Akkaunt qidirish")
    markup.add("➕ Elon berish", "📂 Elonlarim")
    markup.add("👨‍💻 Adminlar", "📚 Qoidalar")
    markup.add("💰 Elon narxlari")
    if user_id == ADMIN_ID:
        markup.add("📊 Statistika", "📢 Reklama yuborish")
    return markup

# --- ASOSIY KOMANDALAR ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    ism = message.from_user.first_name
    bot.send_message(
        message.chat.id, 
        f"🌟 <b>Assalomu alaykum, {ism} 🤍!</b>\n\n"
        f"<b>PRO EFUZ SHOP</b> botiga xush kelibsiz. Bu yerda e'lon berish hozirda <b>mutlaqo BEPUL!</b> 😊\n\n"
        f"Marhamat, kerakli bo'limni tanlang:", 
        reply_markup=main_menu(message.chat.id), 
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def admins(message):
    bot.send_message(
        message.chat.id, 
        f"👨‍💻 <b>Bosh admin:</b> @davlatbekturgunboyev\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR:</b>\n{GARANTLAR}\n\n"
        f"Takliflar va murojaat uchun bosh adminga yozing! 😊",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "📚 Qoidalar")
def rules(message):
    bot.send_message(
        message.chat.id, 
        f"📚 <b>Garantlarimiz:</b>\n{GARANTLAR}\n\n"
        f"Faqat ishonchli xizmat! Akkaunt toza bo'lishi va qoidalarga amal qilinishi shart! ✅", 
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.text == "💰 Elon narxlari")
def prices(message):
    bot.send_message(
        message.chat.id, 
        "💰 <b>Aksiya:</b> Hozirda e'lon berish <b>mutlaqo BEPUL!</b> 🎉\n\n"
        "Fursatdan foydalanib o'z e'loningizni hoziroq joylang!", 
        parse_mode="HTML"
    )

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
    bot.send_message(message.chat.id, "❓ <b>Qanday turdagi e'lon joylamoqchisiz?</b>", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def handle_type(call):
    ad_type = call.data.split("_")[1]
    user_temp[call.message.chat.id] = {"type": ad_type}
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    if ad_type == "sotish":
        msg = bot.send_message(call.message.chat.id, "📸 <b>Akkaunt rasmini yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, s_photo)
    else:
        msg = bot.send_message(call.message.chat.id, "💵 <b>Budjetingizni kiriting:</b>\n<i>Masalan: 500.000</i>", parse_mode="HTML")
        bot.register_next_step_handler(msg, o_budget)

# SOTISH BOSQICHLARI
def s_photo(message):
    if not message.photo:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "⚠️ Iltimos, rasm yuboring!"), s_photo); return
    user_temp[message.chat.id]['photo'] = message.photo[-1].file_id
    bot.register_next_step_handler(bot.send_message(message.chat.id, "💰 <b>Narxini yozing:</b>"), s_price)

def s_price(message):
    user_temp[message.chat.id]['price'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "🔄 <b>Obmen (Bor/Yo'q):</b>"), s_obmen)

def s_obmen(message):
    user_temp[message.chat.id]['obmen'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "⚠️ <b>Holati (Toza/Bandi):</b>"), s_info)

def s_info(message):
    user_temp[message.chat.id]['info'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "📝 <b>Batafsil ma'lumot:</b>"), s_final)

def s_final(message):
    uid = message.chat.id
    d = user_temp[uid]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    caption = (
        f"🔥 <b>#SOTILADI</b>\n\n💰 <b>Narxi:</b> {d['price']}\n♻️ <b>Obmen:</b> {d['obmen']}\n"
        f"⚠️ <b>Holati:</b> {d['info']}\n📝 <b>Ma'lumot:</b> {message.text}\n"
        f"👤 <b>Murojaat:</b> {contact}\n🤝 <b>Garantlar:</b> {GARANTLAR}"
    )
    sent = bot.send_photo(CHANNEL_ID, d['photo'], caption=caption, parse_mode="HTML")
    save_ad(uid, {'photo': d['photo'], 'caption': caption, 'fast': 2, 'mid': sent.message_id})
    bot.send_message(uid, "🎉 <b>Tabriklaymiz!</b> E'loningiz kanalga joylandi.", reply_markup=main_menu(uid), parse_mode="HTML")

# OLISH BOSQICHLARI
def o_budget(message):
    user_temp[message.chat.id]['budget'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "📝 <b>Qanday akkaunt kerak? To'liq yozing:</b>"), o_final)

def o_final(message):
    uid = message.chat.id
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    caption = (
        f"⚡️ <b>#OLINADI</b>\n\n💵 <b>Budjet:</b> {user_temp[uid]['budget']}\n📝 <b>Ma'lumot:</b> {message.text}\n"
        f"👤 <b>Murojaat:</b> {contact}\n🤝 <b>Garantlar:</b> {GARANTLAR}"
    )
    try:
        bot.send_photo(CHANNEL_ID, OLISH_IMAGE, caption=caption, parse_mode="HTML")
    except:
        bot.send_message(CHANNEL_ID, caption, parse_mode="HTML")
    bot.send_message(uid, "✅ <b>Olish e'loningiz kanalga yuborildi!</b>", reply_markup=main_menu(uid), parse_mode="HTML")

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
        bot.send_message(message.chat.id, "😕 <b>Sizda hali e'lonlar yo'q.</b>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("fast_"))
def handle_fast(call):
    idx = int(call.data.split("_")[1]); uid = str(call.message.chat.id); ads = get_ads()
    if ads[uid][idx]['fast'] > 0:
        ads[uid][idx]['fast'] -= 1
        with open(ADS_DB, "w") as f: json.dump(ads, f)
        bot.send_message(CHANNEL_ID, "⚡️ <b>#FAST</b>\n\nUshbu e'lon egasi shoshilinch sotmoqda!", reply_to_message_id=ads[uid][idx]['mid'])
        bot.answer_callback_query(call.id, "✅ E'loningiz kanal tepasiga ko'tarildi!")
    else:
        bot.answer_callback_query(call.id, "❌ FAST limit tugagan!", show_alert=True)

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
        
