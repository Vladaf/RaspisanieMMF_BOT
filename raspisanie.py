import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

TOKEN = "2102064973:AAHCLdGiqH8fqazNzlpbV-zLQ9sUqKYM-3w"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD = range(3)


def start(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Выберите курс:", reply_markup=reply_markup)
    return FIRST


def start_again(update, _):
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text="Выберите курс:", reply_markup=reply_markup)
    return FIRST


def course(update, _):
    query = update.callback_query
    course = query.data
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=f'{course} курс 1 группа'),
            InlineKeyboardButton("2", callback_data=f'{course} курс 2 группа'),
            InlineKeyboardButton("3", callback_data=f'{course} курс 3 группа'),
            InlineKeyboardButton("4", callback_data=f'{course} курс 4 группа'),
            InlineKeyboardButton("5", callback_data=f'{course} курс 5 группа'),
            InlineKeyboardButton("6", callback_data=f'{course} курс 6 группа'),
        ],
        [
            InlineKeyboardButton("7", callback_data=f'{course} курс 7 группа'),
            InlineKeyboardButton("8", callback_data=f'{course} курс 8 группа'),
            InlineKeyboardButton("9", callback_data=f'{course} курс 9 группа'),
            InlineKeyboardButton("10", callback_data=f'{course} курс 10 группа'),
            InlineKeyboardButton("11", callback_data=f'{course} курс 11 группа'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text="Выберите группу:", reply_markup=reply_markup)
    return SECOND

def group(update, _):
    query = update.callback_query
    course_group = query.data
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data='back')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text=f"{course_group}")
    query.message.reply_photo(photo=open(f'static/{course_group}.jpg', 'rb'), reply_markup=reply_markup)
    return THIRD



if __name__ == '__main__':
    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(course),
            ],
            SECOND: [
                CallbackQueryHandler(group),
            ],
            THIRD: [
                CallbackQueryHandler(start_again),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()