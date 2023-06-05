from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types

from create_bot import bot, dp, db
from messages import register_msg
from buttons import register_btn, menu_btn
from states import ChangeState


#Начинаем тест, запрашиваем пол
async def start_test(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	resp = register_msg.get_sex_msg
	keyboard = register_btn.choose_sex

	await bot.delete_message(chat_id, message_id = call.message.message_id)
	await bot.send_message(chat_id, resp, reply_markup = keyboard)
	await ChangeState.get_sex.set()


#Устанавливаем пол и запрашиваем возраст
async def get_sex_func(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	await state.set_data({'sex': call.data})

	await bot.delete_message(chat_id, message_id = call.message.message_id)
	await bot.send_message(chat_id, register_msg.get_age_msg)
	await ChangeState.get_age.set()


#Устанавливаем возраст и запрашиваем страну
async def get_age_func(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	await bot.delete_message(chat_id, message_id = msg.message_id-1)
	await bot.delete_message(chat_id, message_id = msg.message_id)
	try:
		age = int(msg.text)
		if age >= 8 and age <= 99:
			await state.update_data({'age': age})
			await bot.send_message(chat_id, register_msg.get_country_msg, reply_markup = register_btn.select_country)
			await ChangeState.get_country.set()

		else:
			await bot.send_message(chat_id, register_msg.get_age_msg_away)
	except ValueError:
		await bot.send_message(chat_id, register_msg.get_age_msg_away)


#Устанавливаем страну и запрашиваем комнату
async def get_country_func(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	await state.update_data({'country': call.data})
	await bot.delete_message(chat_id, message_id = call.message.message_id)

	all_rooms = db.select({'table': 'rooms', 'type': 'all'})
	keyboard = types.InlineKeyboardMarkup()
	for i in all_rooms:
		btn = types.InlineKeyboardButton(text = str(i[0]), callback_data = str(i[1]))
		keyboard.add(btn)

	await bot.send_message(chat_id, register_msg.get_room_msg, reply_markup = keyboard)
	await ChangeState.get_room.set()


#Устанавливаем комнату и завершаем тест
async def get_room_func(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	await state.update_data({'room': call.data})
	await bot.delete_message(chat_id, message_id = call.message.message_id)
	states_memory = await state.get_data()

	rooms_rule = db.select({'table': 'rooms', 'type': 'one', 'call_back': states_memory['room']})
	await bot.send_message(chat_id, rooms_rule[2])
	await bot.send_message(chat_id, register_msg.ending.replace("Регистрация прошла", "Изменения применены"), reply_markup = menu_btn.main_menu)

	db.update({
		'table': 'users',
		'where': {'user_id': chat_id},
		'colamns': {
			'room': call.data,
			'age': states_memory['age'],
			'sex': states_memory['sex'],
			'country': states_memory['country'],
		}
	})

	await state.finish()


def register_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(start_test, lambda c: c.data == "let_change", state = None)
	dp.register_callback_query_handler(get_sex_func, lambda c: c.data, state = ChangeState.get_sex)
	dp.register_message_handler(get_age_func, state = ChangeState.get_age)
	dp.register_callback_query_handler(get_country_func, lambda c: c.data, state = ChangeState.get_country)
	dp.register_callback_query_handler(get_room_func, lambda c: c.data, state = ChangeState.get_room)