import logging
import subprocess
import glob
import os
from wakeonlan import send_magic_packet
from telebot import types
from config import bot

TELEGRAM_CHAT_ID = int(os.environ.get('TELEGRAM_CHAT_ID'))

# Obtém a variável de ambiente 'DEVICES'
DEVICES = []
for device in os.getenv('DEVICES').split(','):
  # Expande os padrões usando glob
  DEVICES.extend(glob.glob(device))

def config_commands_server():
  #Command /server
  @bot.message_handler(commands=['server'])
  def server(message): 
    logging.info(message.chat.id)
    logging.info(TELEGRAM_CHAT_ID)
    if message.chat.id == TELEGRAM_CHAT_ID:
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      status = types.KeyboardButton("Status")
      disk_space = types.KeyboardButton("Disk Space")
      wake_server = types.KeyboardButton("Wake Server")
      markup.add(status, disk_space, wake_server)

      bot.send_message(message.chat.id, "Selecione uma opção:", reply_markup=markup)
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
      
  #Status
  @bot.message_handler(func=lambda message: message.text == "Status")
  def status(message):
    if message.chat.id == TELEGRAM_CHAT_ID:
      ip_address = os.environ.get('IP_HOME_SERVER')
      process = subprocess.Popen(['ping', '-a', ip_address, '-n', '4'],
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()
      
      callback_message = ''
      
      if len(stderr) > 0:
        callback_message = '😭 Ocorreu um erro ao verificar status do servidor 😭 {}'.format(stderr)
      else:
        # Se não houve erro, verifica a resposta do ping
        if "TTL" in str(stdout):
          callback_message = "😁 Servidor está ativo ✅"
        else:
          callback_message = "😗 Servidor não está ativo ❌"
        
      bot.send_message(message.chat.id, callback_message)
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
      
  #Disk Space
  @bot.message_handler(func=lambda message: message.text == "Disk Space")
  def disk_space(message):
    if message.chat.id == TELEGRAM_CHAT_ID:
      process = subprocess.Popen(['df', '-h'] + DEVICES,
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
      stdout, stderr = process.communicate()
      callback_message = ''
      
      if len(stderr) > 0:
        callback_message = '😭 Ocorreu um erro ao verificar espaço em disco 😭 {}'.format(stderr)
      else:
        # Decodifica e remove espaços extras no início e fim
        stdout_decoded = stdout.decode().strip()
        callback_message = f"<pre>{stdout_decoded}</pre>"
        
      bot.send_message(message.chat.id, callback_message, parse_mode='HTML')
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
      
  #Wake Server
  @bot.message_handler(func=lambda message: message.text == "Wake Server")
  def wake_server(message):
    if message.chat.id == TELEGRAM_CHAT_ID:
      wake_on_lan_macs = os.environ.get('WAKE_ON_LAN_MACS_SERVERS').split(',')
      send_magic_packet(*wake_on_lan_macs)
      callback_message = '👌 Ligando Servidor... 👌'
          
      bot.send_message(message.chat.id, callback_message)
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")

   @bot.message_handler(func=lambda message: message.text == "Wake My PC")
  def wake_server(message):
    if message.chat.id == TELEGRAM_CHAT_ID:
      wake_on_lan_macs = os.environ.get('WAKE_ON_LAN_MACS_MY_PC').split(',')
      send_magic_packet(*wake_on_lan_macs)
      callback_message = '👌 Ligando Meu Computador... 👌'
          
      bot.send_message(message.chat.id, callback_message)
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
