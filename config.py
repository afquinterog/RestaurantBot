import telebot
import logging
import os
from decouple import config

#########################################################

# Versión del bot
VERSION = 0.1

# Obtiene el token desde el archivo de configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') or config('TELEGRAM_TOKEN')

#########################################################

# Crea el objeto bot utilizando el token
bot = telebot.TeleBot(TELEGRAM_TOKEN)    

# Determina el nivel de los mensajes que se van a mostrar (debug)
telebot.logger.setLevel(logging.INFO)

#########################################################