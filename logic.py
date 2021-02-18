#########################################################
# Gestion de Paquetes
import database.db as db
from models.User import User
from models.Order import Order
from models.Item import Item
from models.OrderItem import OrderItem
from datetime import datetime
from sqlalchemy import extract

#########################################################
# Acerca del Bot
def get_about_this (VERSION):
	response = (
				f"\U0001F916 Pedidos UAM Bot (pyTelegramBot) v{VERSION}"
				"\n\n"
				"*Desarrollado por:*\n"
				"Alvaro Perez N <alvaro.perezn@autonoma.edu.co>\n"
				"Andres F Quintero <rocoutp@gmail.com>\n"
				"Hernando Roman <hernando.romang@autonoma.edu.co>"
				)
	
	return response

#########################################################
# Ayuda del Bot - Comandos Disponibles

def get_help_message ():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "\U0001F916 *Generales* \n"
        "*/start* - Registra el usuario y permite iniciar pedido (obligatorio)\n"
        "*/help* - Muestra el mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n\n"

        "\U0001F916 *Comandos Clientes* \n"
        "*Ver Platos|VP * - Muestra la lista de platos\n"
        "*Hacer Pedido|HP {indice} {cantidad} * - Agregar el plato al carrito de compra\n"
        "*Pedido|P* - Mostrar los productos del carrito de compra\n"
        "*Comprar|C* - Compra los productos del carrito\n"
        "*Eliminar Plato Pedido|EPP {indice}* - Elimina el plato del carrito de compra\n"
        "*Historial|H* - Muestra el historial de compra\n\n"

        "\U0001F916 *Comandos Administrador* \n"
        "*Ver Platos|VP * - Muestra la lista de platos\n"
        "*Nuevo Plato|NP {nombre} {valor} * - Agrega un nuevo plato al Menu\n"
        "*Activar Plato|AP {indice} * - Activa el plato en el Menu\n"
        "*Inactivar Plato|IP {indice} * - Inactiva un plato en el Menu\n"
    )
    return response

#########################################################
# Inicio del Bot

def get_welcome_message(bot_data):
    response = (
    f"\U0001F916 Hola, soy *{bot_data.first_name}* "
    f"también conocido como *{bot_data.username}*.\n\n"
    "¡Estoy aquí para ayudarte a registrar tus pedidos!"
    )

    return response

def register_user(user_id):
    user = db.session.query(User).get(user_id)
    db.session.commit()
    if user == None and not is_admin(user_id):
        user = User(user_id, User.USER)
        db.session.add(user)
        db.session.commit()
        return True

    create_admin_user(1477919358)
    return False

def create_admin_users(user_id):
    user = db.session.query(User).get(user_id)
    db.session.commit()

    if user == None:
        user = User(user_id, User.ADMIN)
        db.session.add(user)
        db.session.commit()

def is_admin(user_id):
    admins = [1477919358]
    return user_id in admins

def list_users():
    users = db.session.query(User).all()
    return users

#########################################################
# Agregar un Plato el Menu del Restaurante - US02.1

def add_item(user_id, name, value):
    if is_admin(user_id):
        if value <= 0:
            return False
        item = Item(name, value, Item.ITEM_ACTIVE, user_id)
        db.session.add(item)
        db.session.commit()
        return True
    return False

def get_fallback_message (text):
	response = f"\U0001F648 No entendí lo que me acabas de decir.\n Utiliza la Ayuda /help para los Ver Comandos"
	return response