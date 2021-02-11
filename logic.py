#########################################################

def get_about_this (VERSION):
	response = (
				f"Simple Expenses Bot (pyTelegramBot) v{VERSION}"
				"\n\n"
				"Desarrollado por:\n"
				"Alvaro Perez N <alvaro.perezn@autonoma.edu.co>\n"
				"Andres F Quintero <rocoutp@gmail.com>\n"
				"Hernando Roman <hernando.romang@autonoma.edu.co>"
				)
	
	return response

#########################################################

def get_help_message ():
	response = (
				"Estos son los comandos y órdenes disponibles:\n"
				"\n"
				"*/start* - Inicia la interacción con el bot (obligatorio)\n"
				"*/help* - Muestra este mensaje de ayuda\n"
				"*/about* - Muestra detalles de esta aplicación\n"
			)

	return response

#########################################################

def get_welcome_message (bot_data):
	response = (
				f"Hola, soy *{bot_data.first_name}* "
				f"también conocido como *{bot_data.username}*.\n\n"
				"¡Estoy aquí para ayudarte a Gestionar los Pedidos!"
				)
	
	return response

#########################################################

def get_fallback_message (text):
	response = f"\U0001F648 No entendí lo que me acabas de decir"
	return response

#########################################################