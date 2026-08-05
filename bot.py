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
async def answer_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    answer = int(
        query.data.split("_")[1]
    )

    index = user_data[user_id]["question"]

    question = QUESTIONS[index]

    if answer == question["answer"]:
        user_data[user_id]["score"] += 1

        if question["type"] == "grammar":
            user_data[user_id]["grammar"] += 1
        else:
            user_data[user_id]["vocabulary"] += 1


    user_data[user_id]["question"] += 1


    if user_data[user_id]["question"] < len(QUESTIONS):

        await send_question(
            query,
            user_id
        )

    else:

        await finish_test(
            query,
            user_id
        )



async def finish_test(query, user_id):

    result = user_data[user_id]

    score = result["score"]

    if score <= 7:
        level = "Below A1"

    elif score <= 14:
        level = "A1"

    elif score <= 21:
        level = "A2"

    elif score <= 28:
        level = "B1"

    elif score <= 34:
        level = "B2"

    elif score <= 38:
        level = "C1"

    else:
        level = "C2"


    await query.edit_message_text(
        "🎉 Test Completed!\n\n"
        f"Grammar: {result['grammar']}/20\n"
        f"Vocabulary: {result['vocabulary']}/20\n\n"
        f"Total Score: {score}/40\n\n"
        f"Your CEFR Level: {level}\n\n"
        "Thank you for using Open Talk Placement Test 🎓"
    )
