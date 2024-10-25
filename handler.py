from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from db import add_student, student_exists, add_scores, get_scores
from constants import (ENTER_FIRST_NAME, ENTER_LAST_NAME, WELCOME_BACK, STUDENT_REGISTERED, STUDENT_EXISTS, 
                       SELECT_SUBJECT, STUDENT_NOT_FOUND, ENTER_SCORE, SCORE_SAVED, SCORE_SAVE_ERROR, 
                       INVALID_SCORE, INVALID_NUMBER, SCORES_NOT_FOUND, PROCESSING_ERROR, REGISTER_OR_LOGIN,
                       PREDEFINED_SUBJECTS)

# Состояния для ConversationHandler
FIRST_NAME, LAST_NAME, SCORE = range(3)


async def register_student(update: Update, context: CallbackContext) -> int:
    """
    Регистрация ученика, запрашивая имя.
    """
    await update.message.reply_text(ENTER_FIRST_NAME)
    return FIRST_NAME


async def get_first_name(update: Update, context: CallbackContext) -> int:
    """
    Сохраняет имя ученика и запрашивает фамилию.
    """
    context.user_data['first_name'] = update.message.text
    await update.message.reply_text(ENTER_LAST_NAME)
    return LAST_NAME


async def get_last_name(update: Update, context: CallbackContext) -> int:
    """
    Сохраняет фамилию ученика и проверяет его существование в базе данных.
    Если ученик не существует, регистрирует его.
    """
    context.user_data['last_name'] = update.message.text
    first_name = context.user_data['first_name']
    last_name = context.user_data['last_name']
    if student_exists(first_name, last_name):
        await update.message.reply_text(WELCOME_BACK.format(first_name=first_name, last_name=last_name))
    else:
        if add_student(first_name, last_name):
            await update.message.reply_text(STUDENT_REGISTERED.format(first_name=first_name, last_name=last_name))
        else:
            await update.message.reply_text(STUDENT_EXISTS.format(first_name=first_name, last_name=last_name))
    return ConversationHandler.END


async def enter_scores(update: Update, context: CallbackContext) -> int:
    """
    Логика ввода баллов, проверяя регистрацию ученика и предлагая выбрать предмет.
    """
    if await check_user_logged(update, context.user_data):
        first_name = context.user_data['first_name']
        last_name = context.user_data['last_name']

        if student_exists(first_name, last_name):
            keyboard = []
            row = []
            for subject in PREDEFINED_SUBJECTS:
                row.append(InlineKeyboardButton(subject, callback_data=f'{subject}'))
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(SELECT_SUBJECT, reply_markup=reply_markup)
        else:
            await update.message.reply_text(STUDENT_NOT_FOUND.format(first_name=first_name, last_name=last_name))
    return SCORE


async def button(update: Update, context: CallbackContext) -> int:
    """
    Выбор предмета и запрос вввода баллов.
    """
    query = update.callback_query
    await query.answer()
    context.user_data['subject'] = query.data
    await query.edit_message_text(text=ENTER_SCORE.format(subject=query.data))
    return SCORE


async def get_score(update: Update, context: CallbackContext) -> int:
    """
    Обрабатывает ввод баллов, проверяет их корректность и сохраняет в базе данных.
    """
    try:
        score = int(update.message.text)
        if 0 <= score <= 100:
            first_name = context.user_data['first_name']
            last_name = context.user_data['last_name']
            subject = context.user_data['subject']
            if add_scores(first_name, last_name, subject, score):
                await update.message.reply_text(SCORE_SAVED.format(subject=subject, first_name=first_name, last_name=last_name))
            else:
                await update.message.reply_text(SCORE_SAVE_ERROR.format(first_name=first_name, last_name=last_name))
            return ConversationHandler.END
        else:
            await update.message.reply_text(INVALID_SCORE)
            return SCORE
    except ValueError:
        await update.message.reply_text(INVALID_NUMBER)
        return SCORE


async def view_scores(update: Update, context: CallbackContext) -> None:
    """
    Отображает баллы ученика по всем предметам.
    """
    try:
        if await check_user_logged(update, context.user_data):
            first_name = context.user_data['first_name']
            last_name = context.user_data['last_name']
            scores = get_scores(first_name, last_name)

            if scores:
                scores_text = '\n'.join([f'{subject}: {score}' for subject, score in scores])
                await update.message.reply_text(f'Баллы ЕГЭ для ученика "{first_name} {last_name}":\n{scores_text}')
            else:
                await update.message.reply_text(SCORES_NOT_FOUND.format(first_name=first_name, last_name=last_name))

    except ValueError:
        await update.message.reply_text(PROCESSING_ERROR)


async def check_user_logged(update: Update, user_data):
    """
    Проверяет, зарегистрирован ли пользователь.
    """
    if len(user_data) == 0:
        await update.message.reply_text(REGISTER_OR_LOGIN)
        return False
    return True
