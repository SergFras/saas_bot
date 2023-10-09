# -*- coding: utf-8 -*-

#
#	Основные настройки бота
#

TELEGRAM_TOKEN = ""		# Токен телеграм бота


PAYMENTS = {
	"token": "381764678:TEST:58617", 									# Токен платежки
	"price": 299,														# Цена подписки
	"term": 0.1,														# Срок действия подписки (дни)
	"title": "Заголовок подписки",										# Заголовок подписки
	"description": "Описание подписки"  								# Описание подписки
}


ADMIN_ID = 892023960													# ID админа




#
#	Настройки БД
#

DB_HOST = "localhost" 				# IP адрес БД

DB_PORT = 3306						# Порт БД

DB_NAME = "ecopay_main"				# Имя БД

DB_LOGIN = "root"					# Логин БД

DB_PASSWORD = "oaAUS9BaWwYiZX2"		# Пароль БД
