from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from core.database import Database


class TelegramHandlers:
    def __init__(self):
        self.db = Database()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        keyboard = [[InlineKeyboardButton("Помощь", callback_data='help')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Здравствуйте, {user.first_name}! Я ваш помощник. Чем могу быть полезен?",
            reply_markup=reply_markup
        )
        self.db.add_session(update.effective_chat.id, '/start')

    async def help_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        keyboard = [
            [InlineKeyboardButton("Добавить запись", callback_data='add')],
            [InlineKeyboardButton("Мои записи", callback_data='list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Меню помощи:",
            reply_markup=reply_markup
        )
        self.db.add_session(update.effective_chat.id, 'help_menu')

    def get_handlers(self):
        return [
            CommandHandler('start', self.start),
            CallbackQueryHandler(self.help_menu, pattern='^help$')
        ]