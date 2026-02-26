import telebot
from telebot import types
from flask import Flask
import threading
import os
import html
import re
import json
from PIL import Image, ImageDraw
import requests
from io import BytesIO

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

SHABLON_RASM = "https://img.freepik.com/free-vector/gaming-controller-concept-illustration_114360-3162.jpg"
USER_DB = "users_pro.json"

# Garantlar ro'yxati
GARANTLAR = "@davlatbekturgunboyev, @shoniyozov_12, @Giyosov_o22, @ERKINOV277, @OTABEK_LM_10, @Utop41"

# --- BAZA FUNKSIYALARI ---
def save_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        users.append(str(user_id))
        with open(USER_DB, "w") as f:
            json.dump(users, f)

def get_users():
    if not os.path.exists(USER_DB): return []
    with open(USER_DB, "r") as f: return json.load(f)

# --- YORDAMCHI O'ZGARUVCHILAR ---
user_temp = {}
published_ads = {}
news_temp = {}

def clean_text(text):
    if not text: return ""
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'https?://t\.me/\S+', '', text)
    return text.strip()

def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("➕ E'lon berish", "📂 E'lonlarim")
    markup.add("👨‍💻 Adminlar", "📚 Qoidalar")
    markup.add("💰 E'lon narxlari")
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

# --- ADMIN STATISTIKA VA REKLAMA ---
@bot.message_handler(func=lambda m: m.text == "📊 Statistika" and m.chat.id == ADMIN_ID)
def show_stats(message):
    users = get_users()
    bot.send_message(message.chat.id, f"📊 <b>Bot statistikasi:</b>\n\n👤 Jami foydalanuvchilar: <b>{len(users)} ta</b>", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📢 Reklama yuborish" and m.chat.id == ADMIN_ID)
def start_broadcast(message):
    msg = bot.send_message(message.chat.id, "📢 <b>Reklama matnini yuboring:</b>", parse_mode="HTML")
    bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    users = get_users()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text, parse_mode="HTML")
            count += 1
        except: continue
    bot.send_message(ADMIN_ID, f"✅ Reklama <b>{count}</b> kishiga yuborildi.", parse_mode="HTML")

# --- YANGILIKLAR TAHRIRI (ADMIN) ---
@bot.message_handler(content_types=['photo'], func=lambda m: m.chat.id == ADMIN_ID)
def handle_news_photo(message):
    proc = bot.send_message(message.chat.id, "🖌 <b>Rasm tayyorlanmoqda...</b>", parse_mode="HTML")
    file_info = bot.get_file(message.photo[-1].file_id)
    response = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
    img = Image.open(BytesIO(response.content)).convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    draw.text((width - 180, height - 40), CHANNEL_ID, fill=(255, 255, 255))
    bio = BytesIO(); bio.name = 'news.jpg'; img.save(bio, 'JPEG'); bio.seek(0)
    
    cap = clean_text(message.caption if message.caption else "")
    full_cap = f"{cap}\n\n📍 <b>Kanal:</b> {CHANNEL_ID}\n🤝 <b>Garantlar:</b> {GARANTLAR}\n🚀 <b>Bot:</b> @{bot.get_me().username}"
    news_temp[message.chat.id] = {'photo': bio.getvalue(), 'caption': full_cap}
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Kanalga yuborish", callback_data="send_n"),
               types.InlineKeyboardButton("📝 Matnni tahrirlash", callback_data="edit_n"))
    bot.delete_message(message.chat.id, proc.message_id)
    bot.send_photo(message.chat.id, bio.getvalue(), caption=f"✨ <b>Tayyor:</b>\n\n{full_cap}", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["send_n", "edit_n"])
def callback_news(call):
    if call.data == "send_n":
        data = news_temp.get(call.message.chat.id)
        bot.send_photo(CHANNEL_ID, data['photo'], caption=data['caption'], parse_mode="HTML")
        bot.answer_callback_query(call.id, "✅ Kanalga yuborildi!", show_alert=True)
    elif call.data == "edit_n":
        msg = bot.send_message(call.message.chat.id, "📝 Yangi matnni yuboring:", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_edit)

def process_edit(message):
    news_temp[message.chat.id]['caption'] = message.text
    bot.send_message(message.chat.id, "✅ Matn yangilandi! Endi yuborishingiz mumkin.", parse_mode="HTML")

# --- BO'LIMLAR ---
@bot.message_handler(func=lambda m: m.text == "📚 Qoidalar")
def rules(message):
    bot.send_message(message.chat.id, f"📚 <b>Garantlarimiz:</b>\n{GARANTLAR}\n\nFaqat ishonchli xizmat! ✅", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Adminlar")
def admins(message):
    bot.send_message(message.chat.id, f"👨‍💻 <b>Bosh admin:</b> @davlatbekturgunboyev\nTakliflar uchun yozing! 😊", parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "💰 E'lon narxlari")
def prices(message):
    bot.send_message(message.chat.id, "💰 <b>Aksiya:</b> Hozirda e'lon berish <b>mutlaqo BEPUL!</b>", parse_mode="HTML")

# --- E'LON BERISH ---
@bot.message_handler(func=lambda m: m.text == "➕ E'lon berish")
def step1(message):
    bot.send_photo(message.chat.id, SHABLON_RASM, caption="📸 <b>Akkaunt rasmini yuboring:</b>", parse_mode="HTML")
    bot.register_next_step_handler(message, step2)

def step2(message):
    if not message.photo:
        bot.send_message(message.chat.id, "⚠️ Rasm yuboring!"); bot.register_next_step_handler(message, step2); return
    user_temp[message.chat.id] = {'photo': message.photo[-1].file_id}
    bot.send_message(message.chat.id, "💰 <b>Narxini yozing:</b>", parse_mode="HTML")
    bot.register_next_step_handler(message, step3)

def step3(message):
    user_temp[message.chat.id]['price'] = message.text
    bot.send_message(message.chat.id, "📝 <b>Batafsil ma'lumot:</b>", parse_mode="HTML")
    bot.register_next_step_handler(message, step4)

def step4(message):
    uid = message.chat.id
    user_temp[uid]['desc'] = html.escape(message.text)
    user = bot.get_chat(uid); contact = f"@{user.username}" if user.username else f"ID: {uid}"
    d = user_temp[uid]
    caption = f"🔥 <b>#PRO_SOTILADI</b>\n\n💰 <b>Narxi:</b> {d['price']}\n📝 <b>Ma'lumot:</b> {d['desc']}\n👤 <b>Murojaat:</b> {contact}\n🤝 <b>Garantlar:</b> {GARANTLAR}"
    sent_msg = bot.send_photo(CHANNEL_ID, d['photo'], caption=caption, parse_mode="HTML")
    
    if uid not in published_ads: published_ads[uid] = []
    published_ads[uid].append({'photo': d['photo'], 'caption': caption, 'fast_count': 2, 'message_id': sent_msg.message_id})
    bot.send_message(uid, "🎉 <b>Tabriklaymiz!</b> E'lon kanalga joylandi. ✅", reply_markup=main_menu(uid), parse_mode="HTML")
    del user_temp[uid]

@bot.message_handler(func=lambda m: m.text == "📂 E'lonlarim")
def my_ads(message):
    uid = message.chat.id
    if uid in published_ads and published_ads[uid]:
        for idx, ad in enumerate(published_ads[uid]):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f"⚡️ FAST ({ad['fast_count']})", callback_data=f"fast_{uid}_{idx}"))
            bot.send_photo(uid, ad['photo'], caption=ad['caption'], reply_markup=markup, parse_mode="HTML")
    else: bot.send_message(uid, "😕 E'lonlaringiz yo'q.", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("fast_"))
def handle_fast(call):
    _, uid, idx = call.data.split("_"); uid, idx = int(uid), int(idx)
    if published_ads[uid][idx]['fast_count'] > 0:
        msg = bot.send_message(call.message.chat.id, "🚀 <b>Yangi narxni kiriting:</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, finish_fast, uid, idx)
    else: bot.answer_callback_query(call.id, "❌ FAST tugagan!", show_alert=True)

def finish_fast(message, uid, idx):
    yangi_narx = message.text; ad = published_ads[uid][idx]; ad['fast_count'] -= 1
    bot.send_message(CHANNEL_ID, f"⚡️ <b>#PRO_TEZKOR</b>\n💰 <b>Yangi narx:</b> {yangi_narx}", reply_to_message_id=ad['message_id'], parse_mode="HTML")
    bot.send_message(uid, f"✅ Narx yangilandi! (Qoldi: {ad['fast_count']})", parse_mode="HTML")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
          
