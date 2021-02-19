#########################################################
# Gestion de Paquetes
from config import bot, VERSION
from time import sleep
import config
import re 
import logic
import database.db as db
from models.Item import Item         

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

#########################################################
# Acerca del Bot

@bot.message_handler(commands=['about'])
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, logic.get_about_this(config.VERSION), parse_mode="Markdown")
  
	
#########################################################
# Ayuda del Bot - Comandos Disponibles

@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, logic.get_help_message(), parse_mode="Markdown")

#########################################################
# Inicio del Bot

@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, logic.get_welcome_message(bot.get_me()), parse_mode="Markdown")
    bot.send_message(message.chat.id, logic.get_help_message(), parse_mode="Markdown")
    logic.register_user(message.from_user.id)

#########################################################
# Agregar un Plato el Menu del Restaurante - US02.1

@bot.message_handler(regexp=r"^(Nuevo Plato|NP) ([A-Za-z]+) (([0-9]*[.])?[0-9]+)$")
def new_item(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Nuevo Plato|NP) ([A-Za-z]+) (([0-9]*[.])?[0-9]+)$", message.text, re.IGNORECASE)
    name = parts[2]
    value = int(parts[3])
    result = logic.add_item(message.from_user.id, name, value)

    if (result):
        bot.reply_to(message, f"\U0001F372 Hemos creado y activado el nuevo plato: {value}")
    else:
        bot.reply_to(message, "\U000026A0 Tuve problemas registrando la transacción, por favor vuelve a intentarlo. Recuerda que debes ser Admin")

#########################################################
# Ver los Platos del Menu del Restaurante - US01

@bot.message_handler(regexp=r"^(Ver Platos|VP)$")
def list_items(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Ver Platos|VP) ([A-Za-z]+) (([0-9]*[.])?[0-9]+)$", message.text, re.IGNORECASE)
    items = logic.list_items(message.from_user.id)

    if not items:
        text = f"\U0001F916 No tienes platos registradas en el sistema"
    else:
        text = "``` Listado de platos:\n\n"
        for e in items:
            status =  "Activo" if e.status == Item.ITEM_ACTIVE else "Inactivo"
            text += f"| {e.id} | {e.name} | ${e.value} | {status} |\n"

        text += "```"
    
    bot.reply_to(message, text, parse_mode="Markdown")

#########################################################
# Agregar los Productos al Carrito de Compra - US03

@bot.message_handler(regexp=r"^(Hacer Pedido|HP) ([0-9]+) ([0-9]+)$")
def add_basket(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Hacer Pedido|HP) ([0-9]+) ([0-9]+)$", message.text, re.IGNORECASE)
    index = int(parts[2])
    quantity = int(parts[3])

    addedItem = logic.add_basket(message.from_user.id, index, quantity)

    if (addedItem):
        bot.reply_to(message, f"\U0001F916 Hemos agregado el plato: \U0001F372 {addedItem.name} por ${addedItem.value * quantity} a tu pedido: ")
    else:
        bot.reply_to(message, "\U000026A0 Favor verificar que el plato se encuentre activo e intente de nuevo")

#########################################################
# Ver el Listado de Productos del Carrito - US04

@bot.message_handler(regexp=r"^(Pedido|P)$")
def list_items(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Pedido|P)$", message.text, re.IGNORECASE)

    items = logic.getBasketItems(message.from_user.id)

    if not items:
        text = f"\U0001F916 No tienes platos registradas en el pedido actual"
    else:
        total = 0
        text = "``` Platos en el pedido actual:\n\n"
        for key in items:
            item = items[key]
            order_item = logic.getOrderItemById(key, message.from_user.id)
            text += f"| {key} | {item.name} | ${item.value} * {order_item.quantity} \n"
            total = total + (item.value * order_item.quantity)

        text += "\n\n"
        text += f"\U0001F4B0 Total del pedido es: {total}"
        text += "```"
    
    bot.reply_to(message, text, parse_mode="Markdown")

#########################################################
# Comprar los Productos del Carrito - US06

@bot.message_handler(regexp=r"^(Comprar|C)$")
def buy_basket(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Comprar|C)$", message.text, re.IGNORECASE)
    result = logic.buyBasket(message.from_user.id)

    if (result):
        bot.reply_to(message, f"\U00002705 Felicitaciones has comprado tu pedido por un valor de  {result}. Vamos a comenzar a prepararlo. ")
    else:
        bot.reply_to(message, "\U000026A0 Tuve problemas registrando la transacción, por favor vuelve a intentarlo")

#########################################################
# Eliminar Plato del Carrito de Compra - US05

@bot.message_handler(regexp=r"^(Eliminar Plato Pedido|EPP) ([0-9]+)$")
def delete_item_from_basket(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(r"^(Eliminar Plato Pedido|EPP) ([0-9]+)$", message.text, re.IGNORECASE)
    index = int(parts[2])
    result = logic.delete_item_from_basket(message.from_user.id, index)

    if (result):
        bot.reply_to(message, f"\U00002705 Hemos eliminado el plato de tu pedido")
    else:
        bot.reply_to(message, "\U000026A0 Tuve problemas registrando la transacción, por favor vuelve a intentarlo")

#########################################################
# Mensaje por defecto

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)

#########################################################
if __name__ == '__main__':
	bot.polling(timeout=20)

#########################################################