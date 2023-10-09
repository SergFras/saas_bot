import datetime
import time
import logging
import shutil
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled

import sys
sys.path.append('../')
import config
from modules.database import dataBase



class registration(StatesGroup):
	bot_token = State()


async def btn_sub(bot, message, string):
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	btn = types.InlineKeyboardButton(text = f"Месяц подписки - {config.PAYMENTS['price']} руб", callback_data="buy_sub")
	keyboard.insert(btn)

	await bot.send_message(message.from_user.id, 
		f"<b>Здравствуйте, {message.from_user.first_name}!</b>\n\n"\
		f"Чтобы {string}, необходимо приобрести подписку.",
		reply_markup=keyboard)


def day_to_sec(days): 
	return days * 24 * 60 * 60


def time_sub_day(sec, userid):
	time_now = int(time.time())
	time_middle = sec - time_now

	if time_middle <= 0:
		db = dataBase()
		user_stat = db.db_get_user_stat(int(userid))

		if user_stat["account_status"]:
			os.system(f"cd {os.getcwd()}/users/{userid} && pm2 stop {userid}_main.py --interpreter=python3")

			db.db_update_user_stat(userid, "account_status", 0)	
			db.db_update_bot_stat(userid, "bot_status", 0)

		return False
	else:
		dt = str(datetime.timedelta(seconds=time_middle))
		dt = dt.replace("days", "дней")
		dt = dt.replace("day", "дня")

		if "дн" not in dt:
			if ":" in dt[:2]:
				if int(dt[0]) < 6:
					dt += " часа"
			else:
				dt += " часов"

		return dt