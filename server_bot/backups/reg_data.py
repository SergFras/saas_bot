import telebot
import pymysql
#from config import *
import sys
sys.path.append('../../')
import config

print(config.PAYMENTS)

def bot_is_starting(uid, bot_data):
	TELEGRAM_TOKEN = None

	with open("../../config.py", "r") as f:
		token = f.readlines()
		token = token[6]
		token = token.replace("TELEGRAM_TOKEN", "")
		token = token.replace(" ", "")
		token = token.replace("=", "")
		token = token.replace("\n", "")
		token = token.replace("\"", "")
		
		TELEGRAM_TOKEN = token

	bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

	bot_name = bot_data.first_name
	bot_username = bot_data.username

	msg = "Бот запущен!\n\n"\
		f"Имя бота: {bot_name}\n"\
		f"Ссылка на бота: @{bot_username}"

	bot.send_message(uid, msg)


	connection = pymysql.connect(
			host = ip_address_db,
			port = port_db,
			user = login_db,
			password = password_db,
			database = "ecopay_main",
			cursorclass = pymysql.cursors.DictCursor
			)

	with connection.cursor() as cursor:
		user_stat_query = f"SELECT * FROM `users` WHERE userid = {uid}"

		cursor.execute(user_stat_query)
		user = cursor.fetchone()

		if not(user is None):
			user_update_stat_query = f"UPDATE `users` SET bot_name = '@{bot_username}' WHERE userid = {uid}"

			cursor.execute(user_update_stat_query)
			connection.commit()

	connection.close()