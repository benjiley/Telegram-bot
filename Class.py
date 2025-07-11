import telebot
from telebot import types

bot = telebot.TeleBot("8092089557:AAFU69n7rcDEuSb92_rwb_OBJAbIJlf6roo")

# 👇 Sample Lecture in Parts
lecture = [
    "📘 *Part 1:* Introduction to WAEC\n\nWAEC stands for West African Examinations Council.",
    "📘 *Part 2:* Why WAEC is Important\n\nIt is required for admission into most tertiary institutions.",
    "✅ *End of Lecture!* You’re done. Great job!"
]

# Track user's position in the lecture
lecture_index = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    lecture_index[chat_id] = 0
    send_lecture_part(chat_id)

def send_lecture_part(chat_id):
    idx = lecture_index.get(chat_id, 0)
    if idx < len(lecture):
        text = lecture[idx]
        markup = types.InlineKeyboardMarkup()
        if idx < len(lecture) - 1:
            markup.add(types.InlineKeyboardButton("Next ▶️", callback_data="next"))
        else:
            markup.add(types.InlineKeyboardButton("✅ Done", callback_data="done"))
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(chat_id, "✅ Lecture complete!")

@bot.callback_query_handler(func=lambda call: call.data == "next")
def handle_next(call):
    chat_id = call.message.chat.id
    lecture_index[chat_id] += 1
    send_lecture_part(chat_id)

@bot.callback_query_handler(func=lambda call: call.data == "done")
def handle_done(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "🎉 You’ve completed the lecture!")
    lecture_index.pop(chat_id, None)

bot.polling()
