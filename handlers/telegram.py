from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
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

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        keyboard = [
            [InlineKeyboardButton("Добавить запись", callback_data='add_record')],
            [InlineKeyboardButton("Мои записи", callback_data='list_records')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Меню помощи:",
            reply_markup=reply_markup
        )
        self.db.add_session(update.effective_chat.id, 'help_menu')

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        chat_id = update.effective_chat.id
        self.db.add_session(chat_id, text)
        await context.bot.send_message(chat_id=chat_id, text="Запись добавлена!")

    async def handle_add_record(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Введите данные для добавления:")

    def get_handlers(self):
        return [
            CommandHandler('start', self.start),
            CallbackQueryHandler(self.handle_help, pattern='^help$'),
            CallbackQueryHandler(self.handle_add_record, pattern='^add_record$'),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text)
        ]