import os
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from questions import QUESTIONS


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Start Test",
                callback_data="start_test"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Open Talk Placement Test 🎓\n\n"
        "This test evaluates your English level based on CEFR.\n\n"
        "✅ Grammar\n"
        "✅ Vocabulary\n"
        "✅ A1 to C2 Assessment\n\n"
        "Number of Questions: 40\n"
        "Estimated Time: 15 minutes",
        reply_markup=reply_markup
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "start_test":

        user_data[user_id] = {
            "question": 0,
            "score": 0,
            "grammar": 0,
            "vocabulary": 0
        }

        await send_question(
            query,
            user_id
        )


async def send_question(query, user_id):

    index = user_data[user_id]["question"]

    question = QUESTIONS[index]

    buttons = []

    for i, option in enumerate(question["options"]):

        buttons.append(
            [
                InlineKeyboardButton(
                    option,
                    callback_data=f"answer_{i}"
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        f"Question {index+1}/40\n\n"
        f"{question['question']}",
        reply_markup=keyboard
    )
