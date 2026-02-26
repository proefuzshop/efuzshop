import telebot
from telebot import types
import os
import json

# --- SOZLAMALAR ---
TOKEN = "8298795746:AAGkZaREbwwpRijHC4N8UgfUMGYQ7_T2jlc"
ADMIN_ID = 8144030372
CHANNEL_ID = "@PRO_EFUZ_SHOP"
bot = telebot.TeleBot(TOKEN)

# SIZNING ASL ADMINLARINGIZ (Username bo'yicha)
GARANT_TEXT = (
    "◾️ @eFadmin_uz\n"
    "◾️ @eFGarant\n"
    "◾️ @CR7_ISLAM07\n"
    "◾️ @KAMOLXUJA19\n"
    "◾️ @Sarik_CR7\n"
    "◾️ @Cosmos19\n"
    "◾️ @eF_Rasulov"
)

# Olish eloni uchun shablon rasm (Messi/Ronaldo)
OLISH_IMAGE = "https://i.ibb.co/3ykC6W2/olaman-efuz.jpg"

USER_DB = "users_pro.json"
ADS_DB = "published_ads.json"

# --- BAZA FUNKSIYALARI ---
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

# --- ADMINLAR BO'LIMI (100% RASMDAGI DIZAYN) ---
@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def show_admins(message):
    text = (
        "♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"{GARANT_TEXT}\n\n"
        "Faqatgina ushbu adminlarga kanal nomidan javob beriladi."
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💂‍♂️ @eFadmin_uz", url="https://t.me/eFadmin_uz"),
        types.InlineKeyboardButton("💂‍♂️ @eFGarant", url="https://t.me/eFGarant"),
        types.InlineKeyboardButton("💂‍♂️ @CR7_ISLAM07", url="https://t.me/CR7_ISLAM07"),
        types.InlineKeyboardButton("💂‍♂️ @KAMOLXUJA19", url="https://t.me/KAMOLXUJA19"),
        types.InlineKeyboardButton("💂‍♂️ @Sarik_CR7", url="https://t.me/Sarik_CR7"),
        types.InlineKeyboardButton("💂‍♂️ @Cosmos19", url="https://t.me/Cosmos19"),
        types.InlineKeyboardButton("💂‍♂️ @eF_Rasulov", url="https://t.me/eF_Rasulov"),
        types.InlineKeyboardButton("👨‍💻 Dasturchi", url="https://t.me/davlatbekturgunboyev")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

# --- QOIDALAR ---
@bot.message_handler(func=lambda m: m.text == "📚 Qoidalar")
def rules(message):
    text = (
        "Ushbu botdan faqat efootball akkaunt reklamasi uchun foydalaning boshqa har "
        "qanday maqsadda foydalansangiz yoki akkaunt narxini tushirib e'lon bersangiz "
        "e'loningiz o'chirib yuboriladi, butunlay blok bo'lasiz va pulingiz qaytarilmaydi!"
    )
    bot.send_message(message.chat.id, text)

# --- SOTISH ELONI (INTERFEYS) ---
def s_final(message):
    uid = message.chat.id
    d = user_temp[uid]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    
    # Rasmdagi kabi chiroyli dizayn
    caption = (
        f"<b>#SOTILADI</b>\n\n"
        f"💵 <b>Narx:</b> {d['price']} so'm\n"
        f"♻️ <b>Obmen ko'rish:</b> {d['obmen']}\n"
        f"⚠️ <b>Google & Game Center:</b> {d['info']}\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"📋 <b>Qo'shilgan ma'lumot:</b>\n<i>{message.text}</i>\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"{GARANT_TEXT}\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n"
        f"@{bot.get_me().username}"
    )
    sent = bot.send_photo(CHANNEL_ID, d['photo'], caption=caption, parse_mode="HTML")
    save_ad(uid, {'photo': d['photo'], 'caption': caption, 'fast': 2, 'mid': sent.message_id})
    bot.send_message(uid, "🎉 <b>Tabriklaymiz! E'loningiz kanalga joylandi.</b>", reply_markup=main_menu(), parse_mode="HTML")

# --- OLISH ELONI (INTERFEYS) ---
def o_final(message):
    uid = message.chat.id
    budget = user_temp[uid]['budget']
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
    
    # Rasmdagi kabi chiroyli dizayn
    caption = (
        f"<b>#OLINADI #FAQAT_TOZA</b>\n\n"
        f"💵 <b>BUDJET:</b> {budget} so'm\n"
        f"📋 <b>Ma'lumot:</b>\n<i>{message.text}</i>\n"
        f"☎️ <b>Murojaat:</b> {contact}\n\n"
        f"♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        f"{GARANT_TEXT}\n\n"
        f"🔻 <b>ELON BERISH UCHUN BOTIMIZ</b>\n"
        f"@{bot.get_me().username}"
    )
    try:
        bot.send_photo(CHANNEL_ID, OLISH_IMAGE, caption=caption, parse_mode="HTML")
    except:
        bot.send_message(CHANNEL_ID, caption, parse_mode="HTML")
    bot.send_message(uid, "✅ <b>Olish e'loningiz kanalga yuborildi!</b>", reply_markup=main_menu(), parse_mode="HTML")

# --- QOLGAN FUNKSIYALAR ---
@bot.message_handler(func=lambda m: m.text == "🔍 Akkaunt qidirish")
def search_off(message):
    bot.send_message(message.chat.id, "❌ <b>Qidiruv tizimi o'chirilgan!</b>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "➕ Elon berish")
def start_ad(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔺 Sotish eloni", callback_data="type_sotish"),
        types.InlineKeyboardButton("🔻 Olish eloni", callback_data="type_olish")
    )
    bot.send_message(message.chat.id, "❓ <b>Qanday turdagi elon joylamoqchisiz?</b>", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def set_type(call):
    ad_type = call.data.split("_")[1]
    user_temp[call.message.chat.id] = {"type": ad_type}
    if ad_type == "sotish":
        msg = bot.send_message(call.message.chat.id, "📸 <b>Akkaunt rasmini yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, s_photo)
    else:
        msg = bot.send_message(call.message.chat.id, "💵 <b>Budgetingizni kiriting:</b>\n<i>Masalan: 500.000</i>", parse_mode="HTML")
        bot.register_next_step_handler(msg, o_budget)

def s_photo(message):
    if not message.photo:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "⚠️ Rasm yuboring!"), s_photo); return
    user_temp[message.chat.id]['photo'] = message.photo[-1].file_id
    bot.register_next_step_handler(bot.send_message(message.chat.id, "💰 <b>Narxi:</b>"), s_price)

def s_price(message):
    user_temp[message.chat.id]['price'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "🔄 <b>Obmen ko'rish:</b>"), s_obmen)

def s_obmen(message):
    user_temp[message.chat.id]['obmen'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "⚠️ <b>Holati (Toza/Bandi):</b>"), s_info)

def s_info(message):
    user_temp[message.chat.id]['info'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "📝 <b>Batafsil ma'lumot:</b>"), s_final)

def o_budget(message):
    user_temp[message.chat.id]['budget'] = message.text
    bot.register_next_step_handler(bot.send_message(message.chat.id, "📝 <b>Qanday akkaunt kerak? To'liq yozing:</b>"), o_final)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 Xush kelibsiz!", reply_markup=main_menu())

bot.polling(none_stop=True)
    
