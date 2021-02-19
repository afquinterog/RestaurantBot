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

#########################################################
# Ver los Platos del Menu del Restaurante - US01

def list_items(user_id):
    items = db.session.query(
        Item
        ).all()
    db.session.commit()
    return items

#########################################################
# Agregar los Productos al Carrito de Compra - US03

def add_basket(user_id, index, quantity):

    order = getUserBasket(user_id)

    if not order:
        createBasket(user_id)
        order = getUserBasket(user_id)

    item = getItemById(index, user_id)

    if item and item.status == Item.ITEM_ACTIVE:
        #Code without refactor
        #######################################################
        #order.amount = order.amount + item.value
        # Add the order item
        #orderItem = OrderItem(item.id, order.id)
        #db.session.add(orderItem)
        #db.session.commit()

        #Refactor code 
        add_item_to_order(order, item, quantity)
        return item
    return False

def add_item_to_order(order, item, quantity):
    order.amount = order.amount + (item.value * quantity)
    # Add the order item
    orderItem = OrderItem(item.id, order.id, quantity)
    db.session.add(orderItem)
    db.session.commit()

def getUserBasket(user_id):
    order = db.session.query(
        Order
        ).filter_by(
            user_id = user_id
        ).filter_by(
            status = Order.ORDER_BASKET
        ).first()
    db.session.commit()
    return order

def createBasket(user_id):
    item = Order(user_id, Order.ORDER_BASKET)
    db.session.add(item)
    db.session.commit()
    return True

def getItemById(index, user_id):
    item = db.session.query(
        Item
        ).filter_by(
            id = index
        ).first()
    db.session.commit()
    return item

#########################################################
# Ver el Listado de Productos del Carrito - US04

def getBasketItems(user_id):
    order = getUserBasket(user_id)

    if order:
        orderItems = db.session.query(
            OrderItem
            ).filter_by(
                order_id = order.id
            ).all()
        db.session.commit()

        items = {}
        for orderItem in orderItems:
            item = getItemById(orderItem.item_id, user_id)
            items[orderItem.id] = item
        return items

    return None

def getOrderItemById(index, user_id):
    item = db.session.query(
        OrderItem
        ).filter_by(
            id = index
        ).first()
    db.session.commit()
    return item

#########################################################
# Comprar los Productos del Carrito - US06

def buyBasket(user_id):
    basket = getUserBasket(user_id)

    if basket:
        basket.status = Order.ORDER_DONE
        db.session.commit()
        return basket.amount

    return None
    
def delete_order_item_by_id(order, index):
    orderItem = db.session.query(
        OrderItem
        ).filter_by(
            order_id = order.id
        ).filter_by(
            id = index
        ).delete()
    return orderItem

#########################################################
# Eliminar Plato del Carrito de Compra - US05

def delete_item_from_basket(user_id, index):
    order = getUserBasket(user_id)
    
    #Actual code 
    # orderItem = db.session.query(
    #     OrderItem
    #     ).filter_by(
    #         order_id = order.id
    #     ).filter_by(
    #         id = index
    #     ).first()

    #Refactor code 
    orderItem = getOrderItemById(index, user_id)
    item = getItemById(orderItem.item_id, user_id)
    order.amount = order.amount - (item.value * orderItem.quantity)

    #Actual code 
    # orderItem = db.session.query(
    #     OrderItem
    #     ).filter_by(
    #         order_id = order.id
    #     ).filter_by(
    #         id = index
    #     ).delete()
    
    #Refactor code 
    orderItem = delete_order_item_by_id(order, index)
    
    db.session.commit()
    return orderItem

def get_user_orders(user_id):
    orders = db.session.query(
        Order
        ).filter_by(
            user_id = user_id
        ).filter(
            Order.status > 0
        ).all()
    db.session.commit()
    return orders

#########################################################
# Ver Historial de Compras - US07

def get_order_item_from_order(order):
    orderItems = db.session.query(
        OrderItem
        ).filter_by(
            order_id = order.id
        ).all()

    return orderItems

#########################################################
# Activar los Platos del Menu del Restaurante - US02.2

def mark_item_as_active(user_id, index):
    if is_admin(user_id): 
        item = getItemById(index, user_id)
        
        if not item:
            return None
        
        item.status = Item.ITEM_ACTIVE
        db.session.commit()
        return item
    return False

def get_fallback_message (text):
	response = f"\U0001F648 No entendí lo que me acabas de decir.\n Utiliza la Ayuda /help para los Ver Comandos"
	return response