import time
from modules.database import dataBase
from modules.defs import time_sub_day


def check():
	db = dataBase()
	users = db.db_get_all_users_stat()

	for user in users:
		time_sub = time_sub_day(int(user['time_sub']), int(user['userid']))


while True:
	now = time.localtime()

	if now.tm_min == 00:
		check()

	time.sleep(50)