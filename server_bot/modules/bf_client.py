from telethon import TelegramClient, events
import time

api_id = 20823104
api_hash = ""
client = TelegramClient('session', api_id, api_hash)

BOT_NAME = ""
BOT_USER_NAME = "" # must end with -bot


@client.on(events.NewMessage)
async def message_handler(event):
	print(event.raw_text)



async def main():
	await client.send_message('botfather', '/newbot')
	time.sleep(3)
	await client.send_message('botfather', f'{BOT_NAME}')
	time.sleep(3)
	await client.send_message('botfather', f'{BOT_USER_NAME}')
	time.sleep(3)


def init(bname, buname):
	global BOT_NAME
	global BOT_USER_NAME

	BOT_NAME = bname
	BOT_USER_NAME = buname

	with client:
		client.loop.run_until_complete(main())


init("Create test", "saas_test2_bot")

# with client:
# 	client.loop.run_until_complete(main())
	#client.run_until_disconnected()