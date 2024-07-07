from twitch_chat_irc import twitch_chat_irc
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

HOST = "irc.twitch.tv"
PORT = 6667

username = os.getenv("OWNER")
password = os.getenv("PASS")
channel = os.getenv("CHANNEL")
bot_name = os.getenv("BOT_NAME")

connection = twitch_chat_irc.TwitchChatIRC(bot_name, password)

listing_on = False
ratings = {}

def do_something(message):
	global listing_on, ratings

	msg = message['message']
	# print(msg)

	if message['display-name'] == username and msg == "!startrating":
		ratings = {}
		connection.send(channel, "ВВОДИТЕ ОЦЕНКИ:")
		listing_on = True

	if listing_on:
		if message['display-name'] == username and msg == "!endrating":
			if ratings:
				result = round(sum(ratings.values())/len(ratings), int(os.getenv("DECIMAL")))
				connection.send(channel, f"Итоговая оценка: {result}")
			listing_on = False
		else:
			try:
				if 0<int(msg)<11:
					ratings.update({message['display-name']: int(msg)}) 
			except:
				pass

connection.listen(channel, on_message=do_something)
