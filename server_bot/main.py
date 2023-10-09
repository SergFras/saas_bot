# -*- coding: utf-8 -*-
from modules.database import dataBase
from modules.defs import *




def bot_start():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token=config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
	dp = Dispatcher(bot, storage=storage)


	#
	#	Admin's commands
	#

	@dp.message_handler(commands=["account_status"])
	async def add_admin_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		texts = str(message.text).split(" ")

		if (user_stat["useradmin"]) or (int(message.from_user.id) == config.ADMIN_ID):
			if texts[1].isdigit():
				id_user = int(texts[1])
				user_stat = db.db_get_user_stat(id_user)

				if not(user_stat is None):
					if int(texts[2]):
						date_of_pay = str(datetime.date.today())
						time_sub = int(time.time()) + day_to_sec(config.PAYMENTS["term"])

						db.db_update_user_stat(id_user, "account_status", 1)
						db.db_update_user_stat(id_user, "time_sub", time_sub)
						db.db_update_user_stat(id_user, "price_of_pay", config.PAYMENTS["price"])
						db.db_update_user_stat(id_user, "date_of_pay", f"'{date_of_pay}'")

						db.db_update_bot_stat(id_user, "bot_status", 1)
						os.system(f"cd {os.getcwd()}/users/{id_user} && pm2 start {id_user}_main.py --interpreter=python3 -f")

						await bot.send_message(message.from_user.id, f"Пользователь {user_stat['username']} получил подписку!")
					else:
						db.db_update_user_stat(id_user, "account_status", 0)
						db.db_update_user_stat(id_user, "time_sub", "0")

						db.db_update_bot_stat(id_user, "bot_status", 0)
						os.system(f"cd {os.getcwd()}/users/{id_user} && pm2 stop {id_user}_main.py --interpreter=python3 -f")

						await bot.send_message(message.from_user.id, f"Пользователь {user_stat['username']} потерял подписку!")
				else:
					await bot.send_message(message.from_user.id, "Пользователя с таким ID нет в базе данных!")
			else:
				await bot.send_message(message.from_user.id, "ID должен быть числом!")
		else:
			await bot.send_message(message.from_user.id, "У вас недостаточно прав для выполнения данной команды!")


	@dp.message_handler(commands=["add_admin"])
	async def add_admin_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		if (user_stat["useradmin"]) or (int(message.from_user.id) == config.ADMIN_ID):
			if message.text[11:].isdigit():
				id_admin = int(message.text[11:])
				user_stat = db.db_get_user_stat(id_admin)

				if not(user_stat is None):
					db.db_update_user_stat(id_admin, "useradmin", 1)

					await bot.send_message(message.from_user.id, f"Пользователь {user_stat['username']} получил права админа!")
				else:
					await bot.send_message(message.from_user.id, "Пользователя с таким ID нет в базе данных!")
			else:
				await bot.send_message(message.from_user.id, "ID должен быть числом!")
		else:
			await bot.send_message(message.from_user.id, "У вас недостаточно прав для выполнения данной команды!")


	@dp.message_handler(commands=["delete_admin"])
	async def add_admin_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		if (user_stat["useradmin"]) or (int(message.from_user.id) == config.ADMIN_ID):
			if message.text[14:].isdigit():
				id_admin = int(message.text[14:])
				user_stat = db.db_get_user_stat(id_admin)

				if not(user_stat is None):
					db.db_update_user_stat(id_admin, "useradmin", 1)

					await bot.send_message(message.from_user.id, f"Пользователь {user_stat['username']} потерял права админа!")
				else:
					await bot.send_message(message.from_user.id, "Пользователя с таким ID нет в базе данных!")
			else:
				await bot.send_message(message.from_user.id, "ID должен быть числом!")
		else:
			await bot.send_message(message.from_user.id, "У вас недостаточно прав для выполнения данной команды!")


	@dp.message_handler(commands=["delete_user"])
	async def add_admin_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		if (user_stat["useradmin"]) or (int(message.from_user.id) == config.ADMIN_ID):
			if message.text[13:].isdigit():
				id_admin = int(message.text[13:])
				user_stat = db.db_get_user_stat(id_admin)

				if not(user_stat is None):
					db.db_delete_user(id_admin)

					await bot.send_message(message.from_user.id, f"Пользователь {user_stat['username']} удален из базы данных!")
				else:
					await bot.send_message(message.from_user.id, "Пользователя с таким ID нет в базе данных!")
			else:
				await bot.send_message(message.from_user.id, "ID должен быть числом!")
		else:
			await bot.send_message(message.from_user.id, "У вас недостаточно прав для выполнения данной команды!")


	@dp.message_handler(commands=["users"])
	async def get_users_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		if (user_stat["useradmin"]) or (int(message.from_user.id) == config.ADMIN_ID):
			users = db.db_get_all_users_stat()

			msg = f"<b>Всего пользователей: {len(users)}</b>\n\n"

			for user in users:
				time_sub = time_sub_day(int(user['time_sub']), int(user['userid']))

				if time_sub == False:
					time_sub = "Нет подписки"

				last_name = ""
				if user['last_name'] != None:
					last_name = user['last_name']

				msg += ""\
					f"<b>{user['id']}:</b> {user['username']}\n"\
					f"<b>{user['first_name']} {last_name}</b>\n"\
					f"<b>Telegram id:</b> <code>{user['userid']}</code>\n"\
					f"<b>Дата регистрации:</b> {user['date_of_reg']}\n"\
					f"<b>Дата оплаты:</b> {user['date_of_pay']}\n"\
					f"<b>Ссылка на бота:</b> {user['bot_name']}\n"\
					f"<b>Окончание подписки через</b> {time_sub}\n\n"
					# f"<b>Баланс:</b> {user['price_of_pay']}\n"\

			await bot.send_message(message.from_user.id, msg)
		else:
			await bot.send_message(message.from_user.id, "У вас недостаточно прав для выполнения данной команды!")




	#
	#	Users's commands
	#

	@dp.message_handler(commands=["start"])
	async def start_cmd(message: types.Message):
		db = dataBase()
		user_stat = db.db_get_user_stat(int(message.from_user.id))

		if user_stat == None:
			await btn_sub(bot, message, "зарегистрироваться")
		else:
			await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!")


	@dp.callback_query_handler(text="buy_sub")
	async def buy_sub(call: types.CallbackQuery):
		await bot.delete_message(call.from_user.id, call.message.message_id)
		await bot.send_invoice(chat_id=call.from_user.id, title=config.PAYMENTS["title"], description=config.PAYMENTS["description"], payload="month_sub", provider_token=config.PAYMENTS["token"], currency="RUB", start_parameter="saas_bot", prices=[{"label": "Руб", "amount": config.PAYMENTS['price']*100}])


	@dp.pre_checkout_query_handler()
	async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
		await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


	@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
	async def process_pay(message: types.Message):
		if message.successful_payment.invoice_payload == "month_sub":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))

			if user_stat == None:
				await bot.send_message(message.chat.id, 
						"<b>Как создать токен?</b>\n\n"\
						"1. Переходим в @BotFather\n"\
						"2. Затем отправляем <code>/newbot</code>\n"\
						"3. Отправляем желаемое имя бота,\n"\
						"4. Отправляем желаемый никнейм бота\n(должен быть на английском и заканчиваться на <code>_bot</code>)\n\n"\
						"5. Копируем созданный токен(нажать на него)"
						)

				with open("src/create_token.png", "rb") as photo:
					await bot.send_photo(message.chat.id, photo)

				await bot.send_message(message.from_user.id, "Введите токен бота:")
				await registration.bot_token.set()
			else:
				date_of_pay = str(datetime.date.today())
				time_sub = int(time.time()) + day_to_sec(config.PAYMENTS["term"])

				db.db_update_user_stat(message.from_user.id, "account_status", 1)
				db.db_update_user_stat(message.from_user.id, "time_sub", time_sub)
				db.db_update_user_stat(message.from_user.id, "price_of_pay", config.PAYMENTS["price"])
				db.db_update_user_stat(message.from_user.id, "date_of_pay", f"'{date_of_pay}'")

				await bot.send_message(message.from_user.id, "Вы успешно продлили подписку!")

				db.db_update_bot_stat(message.from_user.id, "bot_status", 1)
				os.system(f"cd {os.getcwd()}/users/{message.from_user.id} && pm2 start {message.from_user.id}_main.py --interpreter=python3 -f")


	@dp.message_handler(state=registration.bot_token)
	async def input_bot_token(message: types.Message, state: FSMContext):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.row("Мой профиль", "Мой бот")

		bot_token = message.text

		if (len(bot_token) < 30) and (":" not in bot_token):
			await bot.send_message(message.from_user.id, "Токен бота введён ошибочно!")
			return
		else:
			db = dataBase()

			userid = int(message.from_user.id)
			username = f"@{message.from_user.username}"
			first_name = str(message.from_user.first_name)
			last_name = str(message.from_user.last_name)

			db.db_reg_user(userid, username, bot_token, first_name, last_name)
			db.db_reg_bot(userid, bot_token)

			if not(os.path.isdir(f"users/{message.from_user.id}")):
				os.mkdir(f"users/{message.from_user.id}")

				with open(f"users/{message.from_user.id}/config_client.py", "w") as f:
					f.write(
						f"bot_token = '{bot_token}'\n\n"\
						"ip_address_db = '127.0.0.1'\n\n"\
						"port_db = 3306\n\n"\
						f"name_db = '{message.from_user.id}_db'\n\n"\
						f"login_db = '{config.DB_LOGIN}'\n\n"\
						f"password_db = '{config.DB_PASSWORD}'\n\n"\
						f"admin_chat_id = {message.from_user.id}"
						)

				file_names = next(os.walk(f"client_bot/"), (None, None, []))[2]

				for file_name in file_names:
					if ".sql" not in file_name:
						shutil.copyfile(f"client_bot/{file_name}", f"users/{message.from_user.id}/{file_name}")
				os.rename(f"users/{message.from_user.id}/main.py", f"users/{message.from_user.id}/{message.from_user.id}_main.py")

				db.db_create_for_user(f"{message.from_user.id}_db")
				os.system(f"mysql -u {config.DB_LOGIN} --password={config.DB_PASSWORD} {message.from_user.id}_db < {os.getcwd()}/client_bot/chatbot.sql")

				#os.system(f"osascript -e 'tell app \"Terminal\"\ndo script \"cd {os.getcwd()}/users/{message.from_user.id} && python3 main.py\"\nend tell'")
				os.system(f"cd {os.getcwd()}/users/{message.from_user.id} && pm2 start {message.from_user.id}_main.py --interpreter=python3 -f")

			db.db_update_bot_stat(message.from_user.id, "bot_status", 1)
			db.db_update_user_stat(message.from_user.id, "account_status", 1)

			time_sub = int(time.time()) + day_to_sec(config.PAYMENTS["term"])
			db.db_update_user_stat(message.from_user.id, "time_sub", time_sub)
			db.db_update_user_stat(message.from_user.id, "price_of_pay", config.PAYMENTS["price"])

			await bot.send_message(message.from_user.id, "Вы успешно зарегистрировались!", reply_markup=keyboard)
			await state.finish()


	@dp.message_handler()
	async def on_message_handler(message: types.Message):
		msg = message.text.lower()


		if msg == "my id":
			await bot.send_message(message.from_user.id, f"<code>{message.from_user.id}</code>")


		if msg == "мой профиль":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))

			if not(user_stat == None):
				time_sub = time_sub_day(int(user_stat['time_sub']), int(message.from_user.id))

				if time_sub == False:
					time_sub = "Нет подписки"

				# f"<b>Баланс:</b> {user_stat['price_of_pay']}\n"\
				msg = ""\
					"<b>Ваш профиль:</b>\n\n"\
					f"<b>Дата оплаты:</b> {user_stat['date_of_pay']}\n"\
					f"<b>Окончание подписки через:</b> {time_sub}\n"\
					f"<b>Ссылка на бота:</b> {user_stat['bot_name']}\n\n"\
					f"<i>Дата регистрации: {user_stat['date_of_reg']}</i>"

				await bot.send_message(message.from_user.id, msg)
			else:
				await bot.send_message(message.from_user.id, "Вы не зарегистрированы!\nОтправьте /start")


		if msg == "мой бот":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))

			if not(user_stat == None):
				if user_stat["account_status"] or (user_stat["useradmin"] or user_stat["userid"] == config.ADMIN_ID):
					keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
					keyboard.row("Включить", "Выключить")
					keyboard.row("Меню")

					await bot.send_message(message.from_user.id, "Для управления ботом используйте клавиатуру ниже!", reply_markup=keyboard)
				else:
					await btn_sub(bot, message, "продолжить пользоваться ботом")
			else:
				await bot.send_message(message.from_user.id, "Вы не зарегистрированы!\nОтправьте /start")


		if msg == "меню" or msg == "menu" or msg == "help":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))

			if not(user_stat == None):
				if user_stat["account_status"] or (user_stat["useradmin"] or user_stat["userid"] == config.ADMIN_ID):
					keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
					keyboard.row("Мой профиль", "Мой бот")

					await bot.send_message(message.from_user.id, "Вы перешли в раздел меню!", reply_markup=keyboard)
				else:
					await btn_sub(bot, message, "продолжить пользоваться ботом")
			else:
				await bot.send_message(message.from_user.id, "Вы не зарегистрированы!\nОтправьте /start")


		if msg == "включить":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))
			bot_stat = db.db_get_bot_stat(int(message.from_user.id))

			if not(user_stat == None):
				if user_stat["account_status"] or (user_stat["useradmin"] or user_stat["userid"] == config.ADMIN_ID):
					if bot_stat["bot_status"] == 0:
						db.db_update_bot_stat(message.from_user.id, "bot_status", 1)
						os.system(f"cd {os.getcwd()}/users/{message.from_user.id} && pm2 start {message.from_user.id}_main.py --interpreter=python3 -f")

						await bot.send_message(message.from_user.id, "Бот успешно запущен!")
					else:
						await bot.send_message(message.from_user.id, "Бот уже запущен!")
				else:
					await btn_sub(bot, message, "продолжить пользоваться ботом")
			else:
				await bot.send_message(message.from_user.id, "Вы не зарегистрированы!\nОтправьте /start")


		if msg == "выключить":
			db = dataBase()
			user_stat = db.db_get_user_stat(int(message.from_user.id))

			if not(user_stat == None):
				if user_stat["account_status"] or (user_stat["useradmin"] or user_stat["userid"] == config.ADMIN_ID):
					db.db_update_bot_stat(message.from_user.id, "bot_status", 0)
					os.system(f"cd {os.getcwd()}/users/{message.from_user.id} && pm2 stop {message.from_user.id}_main.py --interpreter=python3 -f")

					await bot.send_message(message.from_user.id, "Бот успешно выключен!")
				else:
					await btn_sub(bot, message, "продолжить пользоваться ботом")
			else:
				await bot.send_message(message.from_user.id, "Вы не зарегистрированы!\nОтправьте /start")


	executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
	print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
	bot_start()

	# while True:
	# 	try:
	# 		print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
	# 		bot_start()
	# 	except:
	# 		print(f"\nBot has been restarted! {str(datetime.datetime.now())[:-10]}\n\n")
	# 		bot_start()