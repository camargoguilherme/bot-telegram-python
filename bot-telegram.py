from config import bot
from commnd_server import config_commands_server

def main():
  config_commands_server()
  bot.infinity_polling()

if __name__ == '__main__':
  main()
