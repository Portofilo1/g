import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ===== НАСТРОЙКИ =====
TOKEN = "8699361720:AAGPx5UdJOTfIf4iSzJdbN0HbNzh-mGvrYg"
ADMIN = "@loxtorp"

bot = telebot.TeleBot(TOKEN)

# ===== ПРАЙСЫ =====
prices = {
    "sim": {
        "МТС": "5$",
        "Мегафон": "4$",
        "Т2": "2.5$",
        "СБЕР": "2.5$",
        "Билайн": "3$"
    },
    "app": {
        "Юмани": "4.5$",
        "Авито макс": "15$",
        "Госуслуги": "15$"
    },
    "buy": {
        "ГК симок": "45$",
        "ГК банков": "60$",
        "Госуслуги": "15$"
    }
}

# ===== МЕНЮ =====
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Симки", "Приложения")
    markup.row("Куплю", "Контакты")
    return markup

def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Назад")
    return markup

# ===== СТАРТ =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "пр, я бот от бандита , выбирай чо нуэно",
        reply_markup=main_menu()
    )

# ===== ОБРАБОТКА КНОПОК МЕНЮ =====
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    msg = message.text
    
    if msg == "Симки":
        markup = InlineKeyboardMarkup()
        for name, price in prices["sim"].items():
            markup.add(InlineKeyboardButton(
                f"{name} - {price}",
                callback_data=f"sim_{name}"
            ))
        markup.add(InlineKeyboardButton(
            "Админ",
            url=f"https://t.me/{ADMIN.replace('@', '')}"
        ))
        bot.send_message(
            message.chat.id,
            "Выбери оператора:",
            reply_markup=markup
        )
    
    elif msg == "Приложения":
        markup = InlineKeyboardMarkup()
        for name, price in prices["app"].items():
            markup.add(InlineKeyboardButton(
                f"{name} - {price}",
                callback_data=f"app_{name}"
            ))
        markup.add(InlineKeyboardButton(
            "Админ",
            url=f"https://t.me/{ADMIN.replace('@', '')}"
        ))
        bot.send_message(
            message.chat.id,
            "Выбери приложение:",
            reply_markup=markup
        )
    
    elif msg == "Куплю":
        markup = InlineKeyboardMarkup()
        for name, price in prices["buy"].items():
            markup.add(InlineKeyboardButton(
                f"{name} - {price}",
                callback_data=f"buy_{name}"
            ))
        markup.add(InlineKeyboardButton(
            "Админ",
            url=f"https://t.me/{ADMIN.replace('@', '')}"
        ))
        bot.send_message(
            message.chat.id,
            "Что купить:",
            reply_markup=markup
        )
    
    elif msg == "Контакты":
        bot.send_message(
            message.chat.id,
            f"Админ: {ADMIN}",
            reply_markup=back_menu()
        )
    
    elif msg == "Назад":
        bot.send_message(
            message.chat.id,
            "Главное меню:",
            reply_markup=main_menu()
        )

# ===== ОБРАБОТКА ИНЛАЙН КНОПОК =====
@bot.callback_query_handler(func=lambda call: True)
def handle_inline(call):
    data = call.data
    
    if data.startswith("sim_"):
        name = data.replace("sim_", "")
        price = prices["sim"].get(name, "?")
        bot.send_message(
            call.message.chat.id,
            f"{name}\nЦена: {price}\n\nЗаказ: {ADMIN}",
            reply_markup=back_menu()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("app_"):
        name = data.replace("app_", "")
        price = prices["app"].get(name, "?")
        bot.send_message(
            call.message.chat.id,
            f"{name}\nЦена: {price}\n\nЗаказ: {ADMIN}",
            reply_markup=back_menu()
        )
        bot.answer_callback_query(call.id)
    
    elif data.startswith("buy_"):
        name = data.replace("buy_", "")
        price = prices["buy"].get(name, "?")
        bot.send_message(
            call.message.chat.id,
            f"{name}\nЦена: {price}\n\nЗаказ: {ADMIN}",
            reply_markup=back_menu()
        )
        bot.answer_callback_query(call.id)

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("Бот работает...")
    bot.infinity_polling()