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
        "✅ A1 to C1 Assessment\n\n"
        "Number of Questions: 40\n"
        "Estimated Time: 15 minutes",
        reply_markup=reply_markup
    )
