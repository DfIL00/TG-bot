from telegram.ext import ApplicationBuilder
from handlers.telegram import TelegramHandlers
import os
from dotenv import load_dotenv

load_dotenv()

class Bot:
    def __init__(self):
        self.token = os.getenv("BOT_TOKEN")
        self.app = ApplicationBuilder().token(self.token).build()
        self.handlers = TelegramHandlers()

    def setup_handlers(self):
        for handler in self.handlers.get_handlers():
            self.app.add_handler(handler)

    def run(self):
        self.setup_handlers()
        self.app.run_polling()

if __name__ == "__main__":
    bot = Bot()
    bot.run()