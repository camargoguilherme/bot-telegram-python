import logging
import os
import telebot
from telebot import types

from dotenv import load_dotenv

bot: telebot.TeleBot
  
load_dotenv()

# Setup logging
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Check if the required environment variables are set
required_values = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
missing_values = [value for value in required_values if os.environ.get(value) is None]
if len(missing_values) > 0:
  logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
  exit(1)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))

bot.set_my_commands([
  types.BotCommand('/start', 'Start Command'),
  types.BotCommand('/server', 'Server Command'),
])
