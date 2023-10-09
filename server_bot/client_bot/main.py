import random
import time
from telebot import TeleBot
from defs import *



########################################################################################################################
########################################################################################################################
bot = TeleBot(token=bot_token)
########################################################################################################################
########################################################################################################################
@bot.callback_query_handler(func= lambda call: True)
def main_callback_query(call):
    try:
        req = call.data.split('_')


        if req[0] == "unseen":
            if req[1] == "partner":
                bot.send_message(call.message.chat.id, f"<i>{choose_do_on_markup}</i>",
                                 reply_markup=main_admin_keyboard, parse_mode="HTML")
                try:
                    bot.delete_message(call.message.chat.id, call.message.id)
                except Exception:
                    pass

        elif req[0] == "next-partner":
            db, sql = start_connection()
            sql.execute(f"SELECT COUNT(*) FROM `Partner`")
            coun = sql.fetchone()[0]
            row = []
            sql.execute(f"select * from `Partner` ORDER BY `ID` LIMIT %s", (int(req[1])+1,))
            while True:
                rows = sql.fetchone()
                if rows is None:
                    break
                row = rows
            close_connection(db, sql)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=change_price_text, callback_data=f"change-price_{row[0]}"),
                       InlineKeyboardButton(text=delete_text, callback_data=f"delete-partner_{row[0]}"))
            if coun > 1+int(req[1]):
                markup.add(InlineKeyboardButton(text=back_go_text, callback_data=f'back-partner_{int(req[1])-1}'),
                    InlineKeyboardButton(text=f'{int(req[1])+1}/{coun}', callback_data='skip'),
                           InlineKeyboardButton(text=next_go_text, callback_data=f'next-partner_{int(req[1])+1}'))
            if coun == 1 + int(req[1]):
                markup.add(InlineKeyboardButton(text=back_go_text, callback_data=f'back-partner_{int(req[1])-1}'),
                    InlineKeyboardButton(text=f'{int(req[1])+1}/{coun}', callback_data='skip'))
            markup.add(InlineKeyboardButton(text=unseen_text, callback_data="unseen_partner"))
            bot.send_message(call.message.chat.id, f"<b>Партнер №{row[0]}</b>\n\n"
                                                    f"<b>ФИО:</b> <i>{row[2]}</i>\n"
                                                    f"<b>Логин ТГ:</b> {row[1]}\n"
                                                    f"<b>Сумма за клиента</b>: <i>{row[3]}</i>",
                                    parse_mode="HTML", reply_markup=markup)
            try:
                bot.delete_message(call.message.chat.id, call.message.id)
            except Exception:
                pass

        elif req[0] == "back-partner":
            db, sql = start_connection()
            sql.execute(f"SELECT COUNT(*) FROM `Partner`")
            coun = sql.fetchone()[0]
            row = []
            sql.execute(f"select * from `Partner` ORDER BY `ID` LIMIT %s", (int(req[1])+1,))
            while True:
                rows = sql.fetchone()
                if rows is None:
                    break
                row = rows
            close_connection(db, sql)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=change_price_text, callback_data=f"change-price_{row[0]}"),
                       InlineKeyboardButton(text=delete_text, callback_data=f"delete-partner_{row[0]}"))
            if coun > 1+int(req[1]) and int(req[1]) != 0:
                markup.add(InlineKeyboardButton(text=back_go_text, callback_data=f'back-partner_{int(req[1])-1}'),
                    InlineKeyboardButton(text=f'{int(req[1])+1}/{coun}', callback_data='skip'),
                           InlineKeyboardButton(text=next_go_text, callback_data=f'next-partner_{int(req[1])+1}'))
            if int(req[1]) == 0 and coun > 1:
                markup.add(InlineKeyboardButton(text=f'{int(req[1])+1}/{coun}', callback_data='skip'),
                           InlineKeyboardButton(text=next_go_text, callback_data='next-partner_1'))
            markup.add(InlineKeyboardButton(text=unseen_text, callback_data="unseen_partner"))
            bot.send_message(call.message.chat.id, f"<b>Партнер №{row[0]}</b>\n\n"
                                                    f"<b>ФИО:</b> <i>{row[2]}</i>\n"
                                                    f"<b>Логин ТГ:</b> {row[1]}\n"
                                                    f"<b>Сумма за клиента</b>: <i>{row[3]}</i>",
                                    parse_mode="HTML", reply_markup=markup)
            try:
                bot.delete_message(call.message.chat.id, call.message.id)
            except Exception:
                pass

        elif req[0] == "change-price":
            create_WaitData()
            db, sql = start_connection()
            sql.execute('select count(*) from `Partner` where `ID` = %s', int(req[1]))
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
            else:
                sql.execute('delete from `WaitData` where `AdminID` = %s', call.message.chat.id)
                sql.execute("insert into `WaitData`(`AdminID`, `ValueData`) values(%s, %s)",
                            (call.message.chat.id, req[1]))
                close_connection(db, sql)
                msg = bot.send_message(call.message.chat.id, f"<i>{new_cost_text}</i>",
                                       parse_mode="HTML", reply_markup=only_back_markup)
                bot.register_next_step_handler(msg, change_partner_SumStep)
                try:
                    bot.delete_message(call.message.chat.id, call.message.id)
                except Exception:
                    pass

        elif req[0] == "delete-partner":
            db, sql=start_connection()
            sql.execute("select count(*) from `Partner` where `ID` = %s", int(req[1]))
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
                bot.send_message(call.message.chat.id, partner_for_delete_text)
                return 0
            else:
                dd, ss=start_connection()
                sql.execute("select * from `ClientPartner` where `PartnerID` = %s", int(req[1]))
                while True:
                    data_client=sql.fetchone()
                    if data_client is None:
                        break
                    ss.execute("delete from `Client` where `ID` = %s", int(data_client[0]))
                close_connection(dd, ss)
                sql.execute("delete from `ClientPartner` where `PartnerID` = %s", int(req[1]))
                sql.execute("delete from `PartnerTelegram` where `PartnerID` = %s", int(req[1]))
                sql.execute("delete from `Partner` where `ID` = %s", int(req[1]))
                close_connection(db, sql)
                bot.send_message(call.message.chat.id, f"<i>{delete_partner_message}</i>",
                                 reply_markup=main_admin_keyboard, parse_mode="HTML")


    except Exception:
        error(traceback.format_exc())
########################################################################################################################
########################################################################################################################
@bot.message_handler(commands=['start'])
def first_enable_bot(message):
    try:
        create_PartnerTelegram()
        if message.chat.id == admin_chat_id:
            bot.send_message(message.chat.id, f"<b>{choose_do_on_markup}</b>", parse_mode="HTML",
                             reply_markup=main_admin_keyboard)
            return 0

        if " " in message.text:
            db, sql = start_connection()
            sql.execute("select count(*) from `Partner` where lower(`LoginTG`) = %s",
                        f"@{message.from_user.username}".lower())
            coun = sql.fetchone()[0]
            close_connection(db, sql)
            if coun == 0:
                return 0
            if message.text.lower().split(' ')[-1] == message.from_user.username.lower():
                bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)
                db, sql = start_connection()
                sql.execute("select count(*) from `PartnerTelegram` where `TelegramID` = %s", message.chat.id)
                if sql.fetchone()[0] == 0:
                    sql.execute("select * from `Partner` where lower(`LoginTG`) = %s",
                                f"@{message.from_user.username}".lower())
                    row = sql.fetchone()
                    sql.execute("insert into `PartnerTelegram`(`PartnerID`, `TelegramID`) values(%s, %s)",
                                (row[0], message.chat.id,))
                    close_connection(db, sql)
                else:
                    close_connection(db, sql)
            else:
                pass

        else:
            db, sql=start_connection()
            sql.execute("select count(*) from `Partner` where lower(`LoginTG`) = %s",
                        f"@{message.from_user.username}".lower())
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
                return 0
            else:
                bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)
                sql.execute("select count(*) from `PartnerTelegram` where `TelegramID` = %s", message.chat.id)
                if sql.fetchone()[0] == 0:
                    sql.execute("select * from `Partner` where lower(`LoginTG`) = %s",
                                f"@{message.from_user.username}".lower())
                    row=sql.fetchone()
                    sql.execute("insert into `PartnerTelegram`(`PartnerID`, `TelegramID`) values(%s, %s)",
                                (row[0], message.chat.id,))
                    close_connection(db, sql)
                else:
                    close_connection(db, sql)
    except Exception:
        error(traceback.format_exc())
########################################################################################################################
########################################################################################################################
@bot.message_handler(commands=['append_partner'])
def append_partner_UsernameStep(message):
    try:
        if message.chat.id == admin_chat_id:
            if message.text.lower() == "назад":
                bot.send_message(message.chat.id, f"<b>{choose_do_on_markup}</b>", parse_mode="HTML",
                                 reply_markup=main_admin_keyboard)

            elif "@" == str(message.text)[0]:
                db, sql = start_connection()
                sql.execute("select count(*) from `Partner` where `LoginTG` = %s", (message.text,))
                if sql.fetchone()[0] == 0:
                    sql.execute("insert into `WaitPartner` (`AdminID`, `LoginTG`, `FullName`, `Sum`) values(%s,%s,%s,%s)",
                                (message.chat.id, message.text, '-', 0))
                    close_connection(db, sql)
                    msg = bot.send_message(message.chat.id, f"<i>{input_fio_partner_text}</i>",
                                           parse_mode="HTML", reply_markup=back_markup)
                    bot.register_next_step_handler(msg, append_partner_FullNameStep)

                else:
                    close_connection(db, sql)
                    msg = bot.send_message(message.chat.id, f"<b>{partner_too_created_text}</b>",parse_mode="HTML")
                    bot.register_next_step_handler(msg, append_partner_UsernameStep)

            else:
                msg=bot.send_message(message.chat.id, f"<b>{start_login_with_text}</b>",parse_mode="HTML")
                bot.register_next_step_handler(msg, append_partner_UsernameStep)

        else:
            pass
    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, append_partner_UsernameStep)


def append_partner_FullNameStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitPartner` where `AdminID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, f"<b>{choose_do_on_markup}</b>", parse_mode="HTML",
                             reply_markup=main_admin_keyboard)

        elif message.text.lower() == "назад":
            db, sql = start_connection()
            sql.execute("delete from `WaitPartner` where `AdminID` = %s", message.chat.id)
            close_connection(db, sql)
            msg = bot.send_message(message.chat.id, f"<i>{append_partner_UsernameStep_text}</i>",
                                   parse_mode="HTML", reply_markup=only_back_markup)
            bot.register_next_step_handler(msg, append_partner_UsernameStep)

        else:
            db, sql = start_connection()
            sql.execute("update `WaitPartner` set `FullName` = %s where `AdminID` = %s", (message.text, message.chat.id))
            close_connection(db, sql)
            msg = bot.send_message(message.chat.id, f"<i>{append_partner_SumStep_text}</i>",
                                   parse_mode="HTML", reply_markup=back_markup)
            bot.register_next_step_handler(msg, append_partner_SumStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, append_partner_FullNameStep)


def append_partner_SumStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitPartner` where `AdminID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, f"<b>{choose_do_on_markup}</b>", parse_mode="HTML",
                             reply_markup=main_admin_keyboard)

        elif message.text.lower() == "назад":
            msg=bot.send_message(message.chat.id, f"<i>{input_fio_partner_text}</i>",
                                 parse_mode="HTML", reply_markup=back_markup)
            bot.register_next_step_handler(msg, append_partner_FullNameStep)

        else:
            if 99999999999 > int(message.text) > 0:
                db, sql = start_connection()
                sql.execute("update `WaitPartner` set `Sum` = %s where `AdminID` = %s",
                            (int(message.text), message.chat.id,))
                sql.execute("select * from `WaitPartner` where `AdminID` = %s order by ID desc", message.chat.id)
                row = sql.fetchone()
                close_connection(db, sql)
                msg = bot.send_message(message.chat.id, f"<b>Подтвердите добавление партнёра:\n\n"
                                                        f"ФИО:</b> <i>{row[3]}</i>\n"
                                                        f"<b>Логин Telegram:</b> {row[2]}\n"
                                                        f"<b>Сумма выплаты:</b> <i>{row[-1]}</i>",
                                       parse_mode="HTML", reply_markup=agree_markup)
                bot.register_next_step_handler(msg, append_partner_AgreeStep)

            else:
                msg = bot.send_message(message.chat.id, f"<b>{input_true_sum_text}</b>",
                                       parse_mode="HTML")
                bot.register_next_step_handler(msg, append_partner_SumStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, f"<b>{input_int_please_text}</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, append_partner_SumStep)


def append_partner_AgreeStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitPartner` where `AdminID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, f"<b>{choose_do_on_markup}</b>", parse_mode="HTML",
                             reply_markup=main_admin_keyboard)

        elif message.text.lower() == "назад":
            msg = bot.send_message(message.chat.id, f"<i>{append_partner_SumStep_text}</i>",
                                   parse_mode="HTML", reply_markup=back_markup)
            bot.register_next_step_handler(msg, append_partner_SumStep)

        elif message.text.lower() == "подтвердить":
            db, sql = start_connection()
            sql.execute('select * from `WaitPartner` where `AdminID` = %s order by `ID` desc', message.chat.id)
            row = sql.fetchone()
            sql.execute("delete from `WaitPartner` where `AdminID` = %s", message.chat.id)
            sql.execute("insert into `Partner`(`LoginTG`, `FullName`, `Sum`) values(%s, %s, %s)",
                        (row[2], row[3], row[4]))
            close_connection(db, sql)
            url = f"https://t.me/{bot.get_me().username}?start={row[2].split('@')[1]}"
            bot.send_message(message.chat.id, f"<i>{row[3]}</i> успешно добавлен/-а в базу партнеров\n\n"
                                              f"<a href='{url}'>Ссылка</a> для партнера:\n{url}",
                             parse_mode="HTML", reply_markup=main_admin_keyboard)

        else:
            msg = bot.send_message(message.chat.id, use_only_agree_text)
            bot.register_next_step_handler(msg, use_only_agree_text)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, append_partner_AgreeStep)
########################################################################################################################
########################################################################################################################
@bot.message_handler(commands=['change_partner_SumStep'])
def change_partner_SumStep(message):
    try:
        if message.text.lower() == "главное меню" or message.text.lower() == "назад":
            db, sql = start_connection()
            sql.execute("delete from `WaitData` where `AdminID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=main_admin_keyboard)

        else:
            if 99999999999 > int(message.text) > 0:
                db, sql = start_connection()
                sql.execute("select * from `WaitData` where `AdminID` = %s order by `ID` desc", message.chat.id)
                row = sql.fetchone()
                sql.execute("delete from `WaitData` where `AdminID` = %s", message.chat.id)
                sql.execute("update `Partner` set `Sum` = %s where `ID` = %s",
                            (int(message.text), int(row[2]),))
                close_connection(db, sql)
                bot.send_message(message.chat.id, f"<i>{sum_for_partner_change_text}</i>",
                                 reply_markup=main_admin_keyboard, parse_mode="HTML")

            else:
                msg = bot.send_message(message.chat.id, f"<b>{input_true_sum_text}</b>",
                                       parse_mode="HTML")
                bot.register_next_step_handler(msg, change_partner_SumStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, f"<b>{input_int_please_text}</b>", parse_mode="HTML")
        bot.register_next_step_handler(msg, change_partner_SumStep)
########################################################################################################################
########################################################################################################################
@bot.message_handler(commands=['create_client_LastNameStep'])
def create_client_LastNameStep(message):
    try:
        if message.text.lower() == "назад":
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)

        else:
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            sql.execute("insert into `WaitClient`(`TelegramID`, `LastName`, `FirstName`, `FatherName`, `Phone`)"
                        " values(%s, %s, %s, %s, %s)", (message.chat.id, message.text, "-", "-", 0,))
            close_connection(db, sql)
            msg = bot.send_message(message.chat.id, create_client_FirstNameStep_text, reply_markup=back_markup)
            bot.register_next_step_handler(msg, create_client_FirstNameStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, create_client_LastNameStep)


def create_client_FirstNameStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)

        elif message.text.lower() == "назад":
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db, sql)
            msg=bot.send_message(message.chat.id, f"<i>{create_client_LastNameStep_text}</i>", parse_mode="HTML",
                                 reply_markup=only_back_markup)
            bot.register_next_step_handler(msg, create_client_LastNameStep)

        else:
            db, sql = start_connection()
            sql.execute("update `WaitClient` set `FirstName` = %s where `TelegramID` = %s",
                        (message.text, message.chat.id,))
            close_connection(db, sql)
            msg = bot.send_message(message.chat.id, create_client_FatherNameStep_text)
            bot.register_next_step_handler(msg, create_client_FatherNameStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, create_client_FirstNameStep)


def create_client_FatherNameStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)

        elif message.text.lower() == "назад":
            msg = bot.send_message(message.chat.id, create_client_FirstNameStep_text, reply_markup=back_markup)
            bot.register_next_step_handler(msg, create_client_FirstNameStep)

        else:
            db, sql = start_connection()
            sql.execute("update `WaitClient` set `FatherName` = %s where `TelegramID` = %s",
                        (message.text, message.chat.id,))
            close_connection(db, sql)
            msg = bot.send_message(message.chat.id, create_client_PhoneStep_text, reply_markup=skip_markup)
            bot.register_next_step_handler(msg, create_client_PhoneStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, create_client_FatherNameStep)


def create_client_PhoneStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)

        elif message.text.lower() == "назад":
            msg = bot.send_message(message.chat.id, create_client_FatherNameStep_text, reply_markup=back_markup)
            bot.register_next_step_handler(msg, create_client_FatherNameStep)

        elif message.text.lower() == "пропустить":
            db, sql=start_connection()
            sql.execute("update `WaitClient` set `Phone` = %s where `TelegramID` = %s",
                        ("-", message.chat.id,))
            sql.execute("select * from `WaitClient` where `TelegramID` = %s order by `ID` desc", message.chat.id)
            row=sql.fetchone()
            close_connection(db, sql)
            phone="-"
            msg=bot.send_message(message.chat.id, f"Подтвердите добавление клиента:\n\n"
                                                  f"Фамилия: {row[2]}\n"
                                                  f"Имя: {row[3]}\n"
                                                  f"Отчество: {row[4]}\n"
                                                  f"Номер телефона: {phone}", reply_markup=agree_markup)
            bot.register_next_step_handler(msg, create_client_AgreeStep)

        else:
            if 12 >= len(message.text) > 10:
                db, sql = start_connection()
                sql.execute("update `WaitClient` set `Phone` = %s where `TelegramID` = %s",
                            (message.text, message.chat.id,))
                sql.execute("select * from `WaitClient` where `TelegramID` = %s order by `ID` desc", message.chat.id)
                row = sql.fetchone()
                close_connection(db, sql)
                phone=phonenumbers.format_number(phonenumbers.parse(row[5], 'RU'), phonenumbers.PhoneNumberFormat.E164)
                msg = bot.send_message(message.chat.id, f"Подтвердите добавление клиента:\n\n"
                                                        f"Фамилия: {row[2]}\n"
                                                        f"Имя: {row[3]}\n"
                                                        f"Отчество: {row[4]}\n"
                                                        f"Номер телефона: {phone}", reply_markup=agree_markup)
                bot.register_next_step_handler(msg, create_client_AgreeStep)

            else:
                msg = bot.send_message(message.chat.id, input_correct_phone_text)
                bot.register_next_step_handler(msg, create_client_PhoneStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, create_client_PhoneStep)


def create_client_AgreeStep(message):
    try:
        if message.text.lower() == "главное меню":
            db, sql = start_connection()
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db, sql)
            bot.send_message(message.chat.id, choose_do_on_markup, reply_markup=partner_keyboard)

        elif message.text.lower() == "назад":
            msg = bot.send_message(message.chat.id, create_client_PhoneStep_text, reply_markup=skip_markup)
            bot.register_next_step_handler(msg, create_client_PhoneStep)

        else:
            db, sql = start_connection()
            sql.execute("select * from `WaitClient` where `TelegramID` = %s", message.chat.id)
            row = sql.fetchone()
            phone = "-"
            if row[5] != "-":
                phone=phonenumbers.format_number(phonenumbers.parse(row[5], 'RU'), phonenumbers.PhoneNumberFormat.E164)
            sql.execute("insert into `Client`(`Surname`, `Name`, `LastName`, `Telephone`, `IsPayment`, `DateCreate`) "
                        "values(%s, %s, %s, %s, %s, %s)", (row[2], row[3], row[4], phone, 0, date.now().date()))
            sql.execute("SELECT LAST_INSERT_ID();")
            last_id = sql.fetchone()[0]
            sql.execute("select * from `PartnerTelegram` where `TelegramID` = %s", message.chat.id)
            rows = sql.fetchone()
            sql.execute("insert into `ClientPartner`(`ClientID`, `PartnerID`) values(%s, %s)", (last_id, rows[1]))
            sql.execute("delete from `WaitClient` where `TelegramID` = %s", message.chat.id)
            close_connection(db,  sql)
            bot.send_message(message.chat.id, agree_append_client_text, reply_markup=partner_keyboard)
    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, create_client_AgreeStep)
########################################################################################################################
########################################################################################################################
@bot.message_handler(commands=['get_data_document_SendStep'])
def get_data_document_SendStep(message):
    try:
        if message.text is not None and message.text.lower() == "назад":
            bot.send_message(message.chat.id, f"<i>{choose_do_on_markup}</i>", parse_mode="HTML",
                             reply_markup=main_admin_keyboard)

        else:
            if message.document is not None:
                file_name=message.document.file_name
                if file_name.split('.')[1] == "xlsx":
                    file_info=bot.get_file(message.document.file_id)
                    downloaded_file=bot.download_file(file_info.file_path)
                    with open(file_name, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    new_file.close()
                    x = get_data_from_xlsx(file_name, bot)
                    print(1)
                    print(x)
                    if x is None or x == "":
                        bot.send_message(message.chat.id, "После проверки данных файла, клиентов на оплату "
                                                          "обнаружено не было. Формирование отчета отклонено",
                                         reply_markup=main_admin_keyboard)
                    else:
                        print(x)
                        bot.send_document(message.chat.id, open(x, "rb"), reply_markup=main_admin_keyboard)

                else:
                    msg=bot.send_message(message.chat.id, f"<b>{send_file_client_info_text}</b>",
                                         parse_mode="HTML")
                    bot.register_next_step_handler(msg, get_data_document_SendStep)

            else:
                msg = bot.send_message(message.chat.id, f"<b>{send_file_client_info_text}</b>",
                                       parse_mode="HTML")
                bot.register_next_step_handler(msg, get_data_document_SendStep)

    except Exception:
        error(traceback.format_exc())
        msg = bot.send_message(message.chat.id, fatal_text)
        bot.register_next_step_handler(msg, get_data_document_SendStep)
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
@bot.message_handler(content_types=['text'])
def main_query_message(message):
    try:
        data = []
        db, sql = start_connection()
        sql.execute(f"SELECT * FROM `Partner`")
        while True:
            row = sql.fetchone()
            if row is None:
                break
            data.append(str(row[1]).lower())
        close_connection(db, sql)

        if message.text.lower() == 'добавить партнера' and message.chat.id == admin_chat_id:
            create_WaitPartner()
            msg = bot.send_message(message.chat.id, f"<i>{append_partner_UsernameStep_text}</i>",
                                   parse_mode="HTML", reply_markup=only_back_markup)
            bot.register_next_step_handler(msg, append_partner_UsernameStep)

        elif message.text.lower() == "my id":
            bot.send_message(message.chat.id, message.chat.id)

        elif message.text.lower() == 'просмотреть партнеров' and message.chat.id == admin_chat_id:
            db, sql = start_connection()
            sql.execute(f"SELECT COUNT(*) FROM `Partner`")
            coun = sql.fetchone()[0]
            if coun == 0:
                close_connection(db, sql)
                bot.send_message(message.chat.id, f"<b>{now_you_dont_have_partner_text}</b>",
                                 reply_markup=main_admin_keyboard)
            else:
                sql.execute(f"select * from `Partner` ORDER BY `ID` LIMIT 1")
                row = sql.fetchone()
                close_connection(db, sql)
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text=change_price_text, callback_data=f"change-price_{row[0]}"),
                           InlineKeyboardButton(text=delete_text, callback_data=f"delete-partner_{row[0]}"))
                if coun > 1:
                    markup.add(InlineKeyboardButton(text=f"1/{coun}", callback_data='skip'),
                               InlineKeyboardButton(text=next_go_text, callback_data=f"next-partner_1"))
                markup.add(InlineKeyboardButton(text=unseen_text, callback_data="unseen_partner"))
                bot.send_message(message.chat.id, f"<b>Партнер №{row[0]}</b>\n\n"
                                                        f"<b>ФИО:</b> <i>{row[2]}</i>\n"
                                                        f"<b>Логин ТГ:</b> {row[1]}\n"
                                                        f"<b>Сумма за клиента</b>: <i>{row[3]}</i>",
                                       parse_mode="HTML", reply_markup=markup)

        elif message.text.lower() == "добавить клиента" and f'@{message.from_user.username}'.lower() in data:
            create_WaitClient()
            db, sql = start_connection()
            sql.execute("select count(*) from `Partner` where lower(`LoginTG`) = %s",
                        f"@{message.from_user.username}".lower())
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
                bot.send_message(message.chat.id, you_not_partner_text)
            else:
                close_connection(db, sql)
                msg = bot.send_message(message.chat.id, f"<i>{create_client_LastNameStep_text}</i>",
                                       parse_mode="HTML",reply_markup=only_back_markup)
                bot.register_next_step_handler(msg, create_client_LastNameStep)

        elif message.text.lower() == "price" and f'@{message.from_user.username}'.lower() in data:
            db, sql = start_connection()
            sql.execute("select count(*) from `Partner` where lower(`LoginTG`) = %s",
                        f"@{message.from_user.username}".lower())
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
                bot.send_message(message.chat.id, you_not_partner_text)
            else:
                sql.execute("select * from `Partner` where lower(`LoginTG`) = %s",
                            f"@{message.from_user.username}".lower())
                row = sql.fetchone()
                close_connection(db, sql)
                bot.send_message(message.chat.id, f"{your_gift_for_client_text} - {row[-1]}")

        elif message.text.lower() == "помощь":
            if message.chat.id == admin_chat_id:
                bot.send_message(message.chat.id, "<b>Список доступных команд:\n\n</b>"
                                                  '"Помощь" - <i>выводит доступные команды</i>\n'
                                                  '"Добавить партнера" - <i>функционал добавления нового партнера в '
                                                  'систему бота\n</i>'
                                                  '"Просмотреть партнеров" - <i>выводит всех партнёров, которые состоят'
                                                  ' в базе бота\n</i>'
                                                  '"Загрузить список клиентов" - <i>функционал для формирования '
                                                  'отчета по клиентам и выплатам партнерам</i>', parse_mode="HTML")

            if f'@{message.from_user.username}'.lower() in data:
                bot.send_message(message.chat.id, "<b>Список доступных команд:\n\n</b>"
                                                  '"Добавить клиента" - <i>функционал добавления клиента\n</i>'
                                                  '"Помощь" - <i>выводит доступные команды</i>\n'                                                  
                                                  '"Price" - <i>выводит размер вашего вознаграждения за клиента</i>'
                                 , parse_mode="HTML")

            else:
                pass

        elif message.text.lower() == "загрузить список клиентов" and message.chat.id == admin_chat_id:
            msg = bot.send_message(message.chat.id, f"<i>{get_data_document_SendStep_text}</i>",
                                   reply_markup=only_back_markup, parse_mode="HTML")
            bot.register_next_step_handler(msg, get_data_document_SendStep)

        elif message.text.lower() == "list" and message.chat.id == admin_chat_id:
            db, sql = start_connection()
            sql.execute("select count(*) from `Partner`")
            if sql.fetchone()[0] == 0:
                close_connection(db, sql)
                bot.send_message(message.chat.id, you_not_partner_text)
            else:
                wait, msg, msg_data = "", "<b>Список партнёров:</b>\n\n", []
                sql.execute("select * from `Partner` Order By `ID`")
                while True:
                    row = sql.fetchone()
                    if row is None:
                        break
                    wait = f"<b>Партнер №{row[0]}</b>\n" \
                           f"<i>ФИО: {row[2]}\n" \
                           f"Логин Telegram: {row[1]}\n" \
                           f"Сумма вознаграждения: {row[-1]}</i>\n\n"
                    if len(msg) >= 1024:
                        msg_data.append(msg)
                        msg = wait
                    else:
                        msg += wait
                close_connection(db, sql)
                if msg != "":
                    msg_data.append(msg)
                for i in range(len(msg_data)):
                    bot.send_message(message.chat.id, msg_data[i], parse_mode="HTML")
                    time.sleep(0.6)

        else:
            if message.chat.id == admin_chat_id:
                x = message.text.split(' ')
                if len(x) >= 4:
                    try:
                        if message.text.split(' ')[-1].lower() == "delet":
                            del x[-1]
                            x = " ".join(x)
                            db, sql = start_connection()
                            sql.execute("select count(*) from `Partner` where lower(`FullName`) = %s", x.lower())
                            if sql.fetchone()[0] == 0:
                                close_connection(db, sql)
                                bot.send_message(message.chat.id, partner_for_delete_text)
                                return 0
                            else:
                                sql.execute("select * from `Partner` where lower(`FullName`) = %s", x.lower())
                                row = sql.fetchone()
                                dd, ss = start_connection()
                                sql.execute("select * from `ClientPartner` where `PartnerID` = %s", int(row[0]))
                                while True:
                                    data_client = sql.fetchone()
                                    if data_client is None:
                                        break
                                    ss.execute("delete from `Client` where `ID` = %s", int(data_client[0]))
                                close_connection(dd, ss)
                                sql.execute("delete from `ClientPartner` where `PartnerID` = %s", int(row[0]))
                                sql.execute("delete from `Partner` where lower(`FullName`) = %s", x.lower())
                                close_connection(db, sql)
                                bot.send_message(message.chat.id,f"<i>{delete_partner_message}</i>",
                                                 reply_markup=main_admin_keyboard, parse_mode="HTML")
                                return 0

                        if message.text.split(' ')[-1].lower() != "delet" and 99999999999 > int(x[-1]) > 0:
                            new_sum = int(x[-1])
                            del x[-1]
                            x = " ".join(x)
                            db, sql = start_connection()
                            sql.execute("select count(*) from `Partner` where lower(`FullName`) = %s", x.lower())
                            if sql.fetchone()[0] == 0:
                                close_connection(db, sql)
                                bot.send_message(message.chat.id, partner_not_found_text)
                                return 0
                            else:
                                sql.execute("update `Partner` set `Sum` = %s where lower(`FullName`) = %s",
                                            (new_sum, x.lower(),))
                                close_connection(db, sql)
                                bot.send_message(message.chat.id, f"<i>{sum_for_partner_change_text}</i>",
                                                 reply_markup=main_admin_keyboard, parse_mode="HTML")
                                return 0
                    except Exception:
                        pass
        """        db, sql = start_connection()
                query = "SELECT COUNT(*) FROM `Partner` WHERE `LoginTG` = %s"
                sql.execute(query, (f"@{message.from_user.username}",))
                if sql.fetchone()[0] == 0:
                    close_connection(db, sql)
                    bot.send_message(message.chat.id, 'Вы не являетесь партнером')
                else:
                    close_connection(db, sql)
                    bot.send_message(message.chat.id, 'Добро пожаловать!')
        """
    except Exception:
        error(traceback.format_exc())
########################################################################################################################
########################################################################################################################
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
########################################################################################################################
########################################################################################################################
if __name__ == '__main__':
    print("Bot has been started")
    from reg_data import bot_is_starting
    bot_is_starting(admin_chat_id, bot.get_me())

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            error(traceback.format_exc())
            time.sleep(0.3)
