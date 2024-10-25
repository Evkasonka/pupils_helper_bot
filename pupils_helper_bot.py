from telegram import Update
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          filters,
                          CallbackContext,
                          CallbackQueryHandler,
                          ConversationHandler)
from handler import (get_first_name,
                     get_last_name,
                     register_student,
                     enter_scores,
                     view_scores,
                     button,
                     get_score)
from constants import WELCOME_MESSAGE
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Состояния для ConversationHandler
FIRST_NAME, LAST_NAME, SCORE = range(3)


async def start_bot(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    await context.bot.send_message(chat_id=chat.id, text=WELCOME_MESSAGE)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    register_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register_student)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_last_name)]
        },
        fallbacks=[],
    )
    enter_score_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('enter_scores', enter_scores)],
        states={
            SCORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_score)],
        },
        fallbacks=[],
    )
    app.add_handler(CommandHandler('start', start_bot))
    app.add_handler(register_conv_handler)
    app.add_handler(enter_score_conv_handler)
    app.add_handler(CommandHandler('view_scores', view_scores))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_bot))

    app.run_polling()


if __name__ == '__main__':
    main()
