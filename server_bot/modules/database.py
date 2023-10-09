import pymysql
import datetime
import sys
sys.path.append('../')
from config import DB_HOST, DB_PORT, DB_LOGIN, DB_PASSWORD, DB_NAME


class dataBase:
	def db_create_for_user(self, db_name):
		connection = pymysql.connect(
			host = DB_HOST,
			port = DB_PORT,
			user = DB_LOGIN,
			password = DB_PASSWORD
			)

		connection.cursor().execute(f"CREATE DATABASE {db_name}")
		connection.close()


	def db_connect(self):
		connection = pymysql.connect(
			host = DB_HOST,
			port = DB_PORT,
			user = DB_LOGIN,
			password = DB_PASSWORD,
			database = DB_NAME,
			cursorclass = pymysql.cursors.DictCursor
			)

		return connection


	def db_disconnect(self, connection):
		connection.close()


	def db_create(self):
		con = self.db_connect()

		with con.cursor() as cursor:
			create_table_query = "CREATE TABLE `users` (id int AUTO_INCREMENT,"\
				"company_id bigint,"\
				"userid bigint,"\
				"username varchar(64),"\
				"first_name text,"\
				"last_name text,"\
				"useradmin int,"\
				"bot_name varchar(64),"\
				"bot_token text,"\
				"account_status int,"\
				"date_of_reg varchar(32),"\
				"date_of_pay varchar(32),"\
				"time_sub bigint,"\
				"price_of_pay float,"\
				"PRIMARY KEY (id));"
			
			cursor.execute(create_table_query)

		self.db_disconnect(con)


	def db_create_bot_options(self):
		con = self.db_connect()

		with con.cursor() as cursor:
			create_table_query = "CREATE TABLE `bots` (id int AUTO_INCREMENT,"\
				"userid bigint,"\
				"bot_status int,"\
				"bot_name text,"\
				"bot_token text,"\
				"PRIMARY KEY (id));"
			
			cursor.execute(create_table_query)

		self.db_disconnect(con)


	def db_reg_user(self, userid, username, bot_token, first_name, last_name):
		date_of_reg = str(datetime.date.today())
		con = self.db_connect()

		with con.cursor() as cursor:
			reg_user_query = f"INSERT INTO `users` (userid, username, useradmin, bot_token, account_status, date_of_reg, first_name, last_name, date_of_pay) VALUES ({userid}, '{username}', 0, '{bot_token}', 0, '{date_of_reg}', '{first_name}', '{last_name}', '{date_of_reg}');"

			cursor.execute(reg_user_query)
			con.commit()

		self.db_disconnect(con)


	def db_reg_bot(self, userid, bot_token):
		date_of_reg = str(datetime.date.today())
		con = self.db_connect()

		with con.cursor() as cursor:
			reg_user_query = f"INSERT INTO `bots` (userid, bot_status, bot_token) VALUES ({userid}, 1, '{bot_token}');"

			cursor.execute(reg_user_query)
			con.commit()

		self.db_disconnect(con)


	def db_get_user_stat(self, userid):
		con = self.db_connect()

		with con.cursor() as cursor:
			user_stat_query = f"SELECT * FROM `users` WHERE userid = {userid}"

			cursor.execute(user_stat_query)
			user = cursor.fetchone()
			
			if user is None:
				self.db_disconnect(con)

				return None
			else:
				self.db_disconnect(con)

				return user


	def db_get_bot_stat(self, userid):
		con = self.db_connect()

		with con.cursor() as cursor:
			user_stat_query = f"SELECT * FROM `bots` WHERE userid = {userid}"

			cursor.execute(user_stat_query)
			bot = cursor.fetchone()
			
			if bot is None:
				self.db_disconnect(con)

				return None
			else:
				self.db_disconnect(con)

				return bot


	def db_update_user_stat(self, userid, update_smth, what_update):
		con = self.db_connect()

		with con.cursor() as cursor:
			user_stat_query = f"SELECT * FROM `users` WHERE userid = {userid}"

			cursor.execute(user_stat_query)
			user = cursor.fetchone()
			
			if not(user is None):
				user_update_stat_query = f"UPDATE `users` SET {update_smth} = {what_update} WHERE userid = {userid}"

				cursor.execute(user_update_stat_query)
				con.commit()
				self.db_disconnect(con)


	def db_update_bot_stat(self, userid, update_smth, what_update):
		con = self.db_connect()

		with con.cursor() as cursor:
			user_stat_query = f"SELECT * FROM `bots` WHERE userid = {userid}"

			cursor.execute(user_stat_query)
			user = cursor.fetchone()
			
			if not(user is None):
				user_update_stat_query = f"UPDATE `bots` SET {update_smth} = {what_update} WHERE userid = {userid}"

				cursor.execute(user_update_stat_query)
				con.commit()
				self.db_disconnect(con)


	def db_get_all_users_stat(self):
		con = self.db_connect()

		with con.cursor() as cursor:
			users_stat_query = f"SELECT * FROM `users`"

			cursor.execute(users_stat_query)
			users = cursor.fetchall()
			self.db_disconnect(con)

			return users


	def db_delete_user(self, userid):
		con = self.db_connect()

		with con.cursor() as cursor:
			delete_user_query = f"DELETE from `users` where userid = {userid}"

			cursor.execute(delete_user_query)
			con.commit()
			self.db_disconnect(con)

		


# db = dataBase()
# db.db_create()

#db = dataBase()
#db.db_create_bot_options()
