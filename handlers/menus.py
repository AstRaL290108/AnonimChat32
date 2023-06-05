from aiogram.dispatcher import Dispatcher
from aiogram import types

from create_bot import bot, dp, db
from messages import menu_msg
from buttons import menu_btn


#Просмотр комнат
async def view_room(msg: types.Message):
	chat_id = msg.chat.id
	rooms = db.select({'table': 'rooms', 'type': 'all'})

	keyboard = types.InlineKeyboardMarkup()
	for i in rooms:
		btn = types.InlineKeyboardButton(text = i[0], callback_data = f"R{i[1]}")
		keyboard.add(btn)

	await bot.send_message(chat_id, menu_msg.main_msg, reply_markup = keyboard)


#Просмотр профиля
async def view_profile(msg: types.Message):
	chat_id = msg.chat.id
	user = list(db.select({'table': 'users', 'type': 'one', 'user_id': chat_id}))
	if user[5] == "men":
		user[5] = "Мужчина"
	if user[5] == "women":
		user[5] = "Женщина"
	
	await bot.send_message(
		chat_id, 
		f"""
#️⃣{chat_id} - Профиль

🌏Страна - {user[6]}
👫Пол - {user[5]}
🔞Возраст - {user[4]}

👍Лайки - {user[8]}
👎Дизлайки - {user[9]}
❗️Жалобы - {user[10]}
		""",
		reply_markup = menu_btn.profile_menu
		)


#Наши контакты
async def our_contacts(msg: types.Message):
	chat_id = msg.chat.id
	await bot.send_message(chat_id, menu_msg.our_contect, reply_markup = menu_btn.our_contacts)


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(view_room, text = "🚪Комнаты", state = None)
	dp.register_message_handler(view_profile, text = "👤Профиль", state = None)
	dp.register_message_handler(our_contacts, text = "☎️Наши контакты", state = None)