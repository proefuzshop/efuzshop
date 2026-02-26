import telebot
from telebot import types
import os
import json

# --- SOZLAMALAR ---
TOKEN = "8298795746:AAGkZaREbwwpRijHC4N8UgfUMGYQ7_T2jlc"
ADMIN_ID = 8144030372
CHANNEL_ID = "@PRO_EFUZ_SHOP"
bot = telebot.TeleBot(TOKEN)

# Siz xohlagan rasm manzilini o'zgaruvchiga olamiz
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
        "Ushbu botdan faqat efootball akkaunt reklamasi uchun foydalaning boshqa har "
        "qanday maqsadda foydalansangiz yoki akkaunt narxini tushirib e'lon bersangiz "
        "e'loningiz o'chirib yuboriladi, butunlay blok bo'lasiz va pulingiz qaytarilmaydi!"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def show_admins(message):
    text = (
        "♻️ <b>OLDI SOTDI GARANT ADMINLAR</b>\n"
        "◾️ @eFadmin_uz\n"
        "◾️ @eFGarant\n"
        "◾️ @CR7_ISLAM07\n"
        "◾️ @KAMOLXUJA19\n"
        "◾️ @Sarik_CR7\n"
        "◾️ @eF_Rasulov\n\n"
        "Faqatgina ushbu adminlarga kanal nomidan javob beriladi."
    )
    bot.send_message(message.chat.id, text, reply_markup=admin_buttons(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "💰 Elon narxlari")
def prices(message):
    text = (
        "🎉 <b>ZO'R YANGILIK!</b>\n\n"
        "Hozirda botimizda <b>AKSIYA</b> ketmoqda. E'lon berish barcha uchun <b>MUTLAQO BEPUL!</b> 🎁\n\n"
        "Fursatdan foydalanib, e'loningizni hoziroq kanalga joylang!"
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
    bot.send_message(message.chat.id, "❓ <b>Qanday turdagi elon joylamoqchisiz?</b>", reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("type_"))
def choose_type(call):
    ad_type = call.data.split("_")[1]
    user_temp[call.message.chat.id] = {"type": ad_type}
    if ad_type == "sotish":
        msg = bot.send_message(call.message.chat.id, "📸 <b>Akkaunt rasmini yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_photo)
    else:
        msg = bot.send_message(call.message.chat.id, "💵 <b>Elon uchun budgetingizni yuboring:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_budget)

# --- SOTISH BOSQICHLARI ---
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
    uid = message.chat.id
    data = user_temp[uid]
    contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {uid}"
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
    sent = bot.send_photo(CHANNEL_ID, data['photo'], caption=caption, parse_mode="HTML")
    save_ad(uid, {'photo': data['photo'], 'caption': caption, 'fast': 2, 'mid': sent.message_id})
    bot.send_message(uid, "✅ E'lon kanalga yuborildi!", reply_markup=main_menu())

# --- OLISH BOSQICHLARI (Tuzatilgan qism) ---
def process_budget(message):
    user_temp[message.chat.id]['budget'] = message.text
    msg = bot.send_message(message.chat.id, "📋 <b>Qanday akkaunt kerakligini to'liq yozing:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, finish_olish)

def finish_olish(message):
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
    # Rasm yuklashda qotib qolmasligi uchun try-except
    try:
        bot.send_photo(CHANNEL_ID, OLISH_IMAGE, caption=caption, parse_mode="HTML")
    except:
        bot.send_message(CHANNEL_ID, caption, parse_mode="HTML")
        
    bot.send_message(uid, "✅ Olish e'loningiz yuborildi!", reply_markup=main_menu())

# --- ELONLARIM ---
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
        bot.send_message(message.chat.id, "🤷‍♂️ <b>Sizda aktiv elon topilmadi!</b>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("fast_"))
def handle_fast(call):
    idx = int(call.data.split("_")[1])
    uid = str(call.message.chat.id)
    ads = get_ads()
    if ads[uid][idx]['fast'] > 0:
        ads[uid][idx]['fast'] -= 1
        with open(ADS_DB, "w") as f: json.dump(ads, f)
        bot.send_message(CHANNEL_ID, "⚡️ <b>#FAST_SOTUV</b>\n\nUshbu elon egasi shoshilinch sotmoqda!", reply_to_message_id=ads[uid][idx]['mid'])
        bot.answer_callback_query(call.id, "✅ Eloningiz kanal tepasiga ko'tarildi!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ FAST imkoniyati tugagan!", show_alert=True)

bot.polling(none_stop=True)
    
