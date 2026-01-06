import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен из environment variables (зададим позже на Render)
TOKEN = os.environ['8307766905:AAFZL43MHWZ-yKxfgOsnQtxhXrt2L1DHVS8']
bot = telebot.TeleBot(8307766905:AAFZL43MHWZ-yKxfgOsnQtxhXrt2L1DHVS8)

app = Flask(__name__)

# Виртуальное состояние
gate_state = "Закрыто 🔒"
light_state = "ВЫКЛ 🌙"

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Открыть ворота 🚀", callback_data="open"),
        InlineKeyboardButton("Закрыть ворота 🔻", callback_data="close")
    )
    markup.add(
        InlineKeyboardButton("Калитка 🚪", callback_data="wicket"),
        InlineKeyboardButton("Частичное ↕️", callback_data="partial")
    )
    markup.add(
        InlineKeyboardButton("Свет ВКЛ 💡", callback_data="light_on"),
        InlineKeyboardButton("Свет ВЫКЛ 🌙", callback_data="light_off")
    )
    markup.add(InlineKeyboardButton("Статус ℹ️", callback_data="status"))
    return markup

# Handlers (как в симуляции)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это управление гаражными воротами.\nНажми кнопки 👇", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global gate_state, light_state

    if call.data == "open":
        if "Закрыто" in gate_state:
            gate_state = "Открыто 🔓"
            light_state = "ВКЛ 💡"
            bot.send_message(call.message.chat.id, "🚀 Ворота открываются!\n💡 Свет включён автоматически")
        else:
            bot.answer_callback_query(call.id, "Уже открыто или в движении")

    # (Добавь остальные как в предыдущем коде: close, wicket, partial, light_on/off, status)
    # Для краткости сократил, но скопируй полностью из моей прошлой симуляции

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=main_menu())

# Webhook роуты
@app.route('/')
def index():
    return "Бот работает! 🚀"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return abort(403)

# Установка webhook при старте (автоматически)
if __name__ == '__main__':
    bot.remove_webhook()
    import time
    time.sleep(1)  # Пауза для Render
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
