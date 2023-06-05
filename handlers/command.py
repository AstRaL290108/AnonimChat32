from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types

from create_bot import bot, dp, db
from messages import register_msg, menu_msg, dialog_msg
from buttons import register_btn, menu_btn
from states import DialogState
from config import hello_sticker


#Комманда старт
async def get_start(msg: types.Message):
	user_id = msg.chat.id
	user = db.select({'user_id': user_id, 'type': 'one', 'table': 'users'})
	
	await bot.send_sticker(user_id, hello_sticker)
	if user is None:
		btn = register_btn.let_test
		resp = register_msg.start_msg.format(username = msg.chat.username)
		await bot.send_message(user_id, resp, reply_markup = btn)
	else:
		await bot.send_message(user_id, menu_msg.main_menu_msg.format(username = msg.chat.full_name), reply_markup = menu_btn.main_menu)


#Комманда стоп
async def get_stop(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']

	feedback_me = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text = "👍Лайк", callback_data = f"l{comp_id}")
	btn2 = types.InlineKeyboardButton(text = "👎Дизлайк", callback_data = f"d{comp_id}")
	btn3 = types.InlineKeyboardButton(text = "❗️Пожаловаться", callback_data = f"r{comp_id}")
	feedback_me.add(btn1, btn2)
	feedback_me.add(btn3)

	feedback_you = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text = "👍Лайк", callback_data = f"l{chat_id}")
	btn2 = types.InlineKeyboardButton(text = "👎Дизлайк", callback_data = f"d{chat_id}")
	btn3 = types.InlineKeyboardButton(text = "❗️Пожаловаться", callback_data = f"r{chat_id}")
	feedback_you.add(btn1, btn2)
	feedback_you.add(btn3)

	await bot.send_message(chat_id, dialog_msg.end_dialog_for_me, reply_markup = feedback_me)
	await bot.send_message(comp_id, dialog_msg.end_dialog_for_you, reply_markup = feedback_you)

	await bot.send_message(user_id, menu_msg.other_main_menu, reply_markup = menu_btn.main_menu)
	await bot.send_message(comp_id, menu_msg.other_main_menu, reply_markup = menu_btn.main_menu)

	await state.finish()

	state_ = dp.current_state(chat=comp_id, user=comp_id)
	await state_.finish()


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(get_start, commands = ["start"], state = None)
	dp.register_message_handler(get_stop, commands = ["stop"], state = DialogState.spanking)