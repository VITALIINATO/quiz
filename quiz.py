from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен бота
TOKEN = "7779914668:AAEuMOeS7yCYKLaAAF6FRHW6ooBwJjTxfEc"

# Вопросы и ответы
questions = [
    {
        "question": "Какой язык программирования используется для создания Telegram-ботов?",
        "options": ["Python", "JavaScript", "C++", "Ruby"],
        "correct_option": 0
    },
    {
        "question": "Какой язык наиболее популярен для веб-разработки?",
        "options": ["Python", "C#", "JavaScript", "R"],
        "correct_option": 2
    }
]

# Хранение состояния пользователя
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Инициализация опроса для пользователя"""
    user_id = update.message.chat_id
    user_data[user_id] = {"score": 0, "question_index": 0}
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка вопроса и вариантов ответа"""
    user_id = update.effective_user.id
    question_index = user_data[user_id]["question_index"]
    question_data = questions[question_index]
    question_text = question_data["question"]

    # Создание клавиатуры с вариантами ответов
    keyboard = [
        [InlineKeyboardButton(option, callback_data=str(i))] for i, option in enumerate(question_data["options"])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=user_id, text=question_text, reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Проверка ответа пользователя и отправка результата"""
    query = update.callback_query
    user_id = query.from_user.id
    question_index = user_data[user_id]["question_index"]
    question_data = questions[question_index]
    user_choice = int(query.data)
    correct_option = question_data["correct_option"]

    # Проверка правильного ответа
    if user_choice == correct_option:
        await query.answer("Ваш ответ верный!")
        user_data[user_id]["score"] += 1
    else:
        correct_answer = question_data["options"][correct_option]
        await query.answer(f"Ваш ответ неверен. Правильный ответ: {correct_answer}")

    # Переход к следующему вопросу или завершение опроса
    if question_index + 1 < len(questions):
        user_data[user_id]["question_index"] += 1
        await ask_question(update, context)
    else:
        score = user_data[user_id]["score"]
        await context.bot.send_message(chat_id=user_id, text=f"Опрос завершен. Количество правильных ответов: {score}/{len(questions)}.")
        await context.bot.send_message(chat_id=user_id, text="Хотите пройти опрос снова? Введите /start.")
        user_data[user_id] = {"score": 0, "question_index": 0}

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_answer))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
