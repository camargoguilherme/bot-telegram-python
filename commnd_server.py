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
  
  
# Função para exibir as opções assim que o bot iniciar
def send_options(chat_id):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  
  # Botões
  status = types.KeyboardButton("Status")
  disk_space = types.KeyboardButton("Disk Space")
  wake_server = types.KeyboardButton("Wake Server")
  wake_my_pc = types.KeyboardButton("Wake My PC")
  cpu_usage = types.KeyboardButton("CPU Usage")

  # Adiciona os botões ao teclado
  markup.add(status, disk_space, wake_server, wake_my_pc, cpu_usage)
  
  # Envia a mensagem com o teclado
  bot.send_message(chat_id, "Selecione uma opção:", reply_markup=markup)

def config_commands_server():
  send_options(TELEGRAM_CHAT_ID)
  # #Command /server
  # @bot.message_handler(commands=['server'])
  # def server(message): 
  #   logging.info(message.chat.id)
  #   logging.info(TELEGRAM_CHAT_ID)
  #   if message.chat.id == TELEGRAM_CHAT_ID:
  #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  #     status = types.KeyboardButton("Status")
  #     disk_space = types.KeyboardButton("Disk Space")
  #     wake_server = types.KeyboardButton("Wake Server")
  #     markup.add(status, disk_space, wake_server)

  #     bot.send_message(message.chat.id, "Selecione uma opção:", reply_markup=markup)
  #   else:
  #     bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
      
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

  #Wake My PC
  @bot.message_handler(func=lambda message: message.text == "Wake My PC")
  def wake_server(message):
    if message.chat.id == TELEGRAM_CHAT_ID:
      wake_on_lan_macs = os.environ.get('WAKE_ON_LAN_MACS_MY_PC').split(',')
      send_magic_packet(*wake_on_lan_macs)
      callback_message = '👌 Ligando Meu Computador... 👌'
          
      bot.send_message(message.chat.id, callback_message)
    else:
      bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")

# Função para pegar o consumo de CPU
@bot.message_handler(func=lambda message: message.text == "CPU Usage")
def cpu_usage(message):
  if message.chat.id == TELEGRAM_CHAT_ID:
    try:
      # Usando o comando 'top' para pegar o consumo de CPU
      process = subprocess.Popen(['top', '-bn1', '|', 'grep', '"%Cpu"'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, shell=True)
      stdout, stderr = process.communicate()
      callback_message = ''

      if len(stderr) > 0:
        callback_message = f'😭 Ocorreu um erro ao verificar o uso de CPU 😭 {stderr.decode()}'
      else:
        stdout_decoded = stdout.decode().strip()
        callback_message = f"<pre>{stdout_decoded}</pre>"

        bot.send_message(message.chat.id, callback_message, parse_mode='HTML')

    except Exception as e:
      bot.send_message(message.chat.id, f"Erro ao obter uso de CPU: {str(e)}")
  else:
    bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")

# Função para pegar o consumo de CPU
@bot.message_handler(func=lambda message: message.text == "CPU Memory")
def cpu_usage(message):
  if message.chat.id == TELEGRAM_CHAT_ID:
    try:
      # Usando o comando 'top' para pegar o consumo de CPU
      process = subprocess.Popen(['top', '-bn1', '|', 'grep', '"%Mem"'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, shell=True)
      stdout, stderr = process.communicate()
      callback_message = ''

      if len(stderr) > 0:
        callback_message = f'😭 Ocorreu um erro ao verificar o uso de Memória 😭 {stderr.decode()}'
      else:
        stdout_decoded = stdout.decode().strip()
        callback_message = f"<pre>{stdout_decoded}</pre>"

        bot.send_message(message.chat.id, callback_message, parse_mode='HTML')

    except Exception as e:
      bot.send_message(message.chat.id, f"Erro ao obter uso de Memória: {str(e)}")
  else:
    bot.reply_to(message, "🤨 Desculpe, você não tem permissão para executar os comandos. 😛")
