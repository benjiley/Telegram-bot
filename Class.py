import telebot
from telebot import types
import random

bot = telebot.TeleBot("8092089557:AAFU69n7rcDEuSb92_rwb_OBJAbIJlf6roo")

# Store student info (as before)
user_data = {}
quiz_state = {}

# Sample WAEC-style questions
questions = [
    {
        "question": "What is the capital of Nigeria?",
        "options": ["Accra", "Nairobi", "Abuja", "Lagos"],
        "answer": "c"
    },
    {
        "question": "Simplify: 2(3x - 4) = ?",
        "options": ["6x - 4", "6x - 8", "5x - 2", "3x - 4"],
        "answer": "b"
    },
    {
        "question": "Which gas do plants use for photosynthesis?",
        "options": ["Oxygen", "Hydrogen", "Carbon Dioxide", "Nitrogen"],
        "answer": "c"
    }
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'name'}
    bot.send_message(chat_id, "Welcome to WAEC Tutorial Bot!\nWhat is your full name?")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    chat_id = message.chat.id
    question = random.choice(questions)
    quiz_state[chat_id] = question

    options = question["options"]
    text = f"📘 *Quiz Time!*\n\n{question['question']}\n"
    text += f"(a) {options[0]}\n(b) {options[1]}\n(c) {options[2]}\n(d) {options[3]}\n\nReply with a/b/c/d"

    bot.send_message(chat_id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()

    # Check if user is answering a quiz
    if chat_id in quiz_state:
        correct_answer = quiz_state[chat_id]["answer"]
        if text == correct_answer:
            bot.send_message(chat_id, "✅ Correct!")
        elif text in ['a', 'b', 'c', 'd']:
            bot.send_message(chat_id, f"❌ Wrong! The correct answer is *{correct_answer.upper()}*.", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "❗Please answer with a, b, c, or d.")
        del quiz_state[chat_id]  # Clear quiz state after answer
        return

    # Continue registration flow
    if chat_id not in user_data:
        bot.send_message(chat_id, "Type /start to register first.")
        return

    step = user_data[chat_id].get('step')

    if step == 'name':
        user_data[chat_id]['name'] = text
        user_data[chat_id]['step'] = 'class'

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("SS1", "SS2", "SS3")
        bot.send_message(chat_id, "Which class are you in?", reply_markup=markup)

    elif step == 'class':
        user_data[chat_id]['class'] = text
        user_data[chat_id]['step'] = 'subjects'
        bot.send_message(chat_id, "List your subjects of interest (separated by commas).")

    elif step == 'subjects':
        user_data[chat_id]['subjects'] = text
        user_data[chat_id]['step'] = 'done'

        name = user_data[chat_id]['name']
        level = user_data[chat_id]['class']
        subjects = user_data[chat_id]['subjects']

        bot.send_message(chat_id, f"✅ Registration complete!\n\n👤 Name: {name}\n🏫 Class: {level}\n📚 Subjects: {subjects}")

    else:
        bot.send_message(chat_id, "You're already registered. Use /quiz to start a test.")

# Start the bot
bot.polling()
