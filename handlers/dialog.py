from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types

from create_bot import bot, dp, db
from messages import dialog_msg, menu_msg
from buttons import dialog_btn, menu_btn
from states import DialogState



#Оценка пользователей
async def set_feedback(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	user = db.select({'table': 'users', 'type': 'one', 'user_id': chat_id})
	if call.data[0] == "l":
		db.update({
			'colamns': {'likes': user[8] + 1},
			'where': {'user_id': chat_id},
			'table': 'users'
		})
		await bot.delete_message(chat_id, message_id = call.message.message_id)
		await bot.send_message(chat_id, dialog_msg.thank_for_feedback)
	elif call.data[0] == "d":
		db.update({
			'colamns': {'dislikes': user[9] + 1},
			'where': {'user_id': chat_id},
			'table': 'users'
		})
		await bot.delete_message(chat_id, message_id = call.message.message_id)
	elif call.data[0] == "r":
		db.update({
			'colamns': {'reports': user[10] + 1},
			'where': {'user_id': chat_id},
			'table': 'users'
		})
		await bot.delete_message(chat_id, message_id = call.message.message_id)


	#Изменение комнаты
	elif call.data[0] == "R":
		new_room = call.data.replace("R", "")
		db.update({
			'table': 'users',
			'where': {'user_id': chat_id},
			'colamns': {'room': new_room}
		})

		await bot.send_message(chat_id, menu_msg.room_changed, reply_markup = menu_btn.main_menu)


#Отменить поиск
async def stop_search_func(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	db.delete({'table': 'wait_list', 'user_id': chat_id})
	await bot.send_message(chat_id, dialog_msg.stop_serch, reply_markup = menu_btn.main_menu)


#Подбор собеседника
async def search_companion_func(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	await bot.send_message(chat_id, dialog_msg.start_search_msg, reply_markup = dialog_btn.close)

	this_user = db.select({'user_id': chat_id, 'type': 'one', 'table': 'users'})
	all_users = db.select({'room': this_user[3], 'type': 'many', 'table': 'wait_list'})

	if all_users is None:
		db.insert_into({
			'table': 'wait_list',
			'user_id': chat_id,
			'room': this_user[3],
			'age': this_user[4],
			'sex': this_user[5],
			'country': this_user[6]	
		})
	else:
		winners = []
		for i in all_users:
			if i[4] == this_user[6]:
				if i[3] != this_user[5]:
					if i[2] >= this_user[4] - 4 and i[2] <= this_user[4] + 4:
						winners.append([i[0], 3])
				else:
					if i[2] >= this_user[4] - 4 and i[2] <= this_user[4] + 4:
						winners.append([i[0], 2])


			elif i[3] != this_user[5]:
				if i[2] >= this_user[4] - 4 and i[2] <= this_user[4] + 4:
					winners.append([i[0], 2])


			elif i[2] >= this_user[4] - 4 and i[2] <= this_user[4] + 4:
				winners.append([i[0], 1])

		
		componion = [0, 0]
		for i in winners:
			if i[1] > componion[1]:
				componion = [i[0], i[1]]

		room = db.select({'table': 'rooms', 'type': 'one', 'call_back': this_user[3]})
		await bot.send_message(chat_id, dialog_msg.go_dialog.format(room = room[0]), reply_markup = types.ReplyKeyboardRemove())
		await bot.send_message(componion[0], dialog_msg.go_dialog.format(room = room[0]), reply_markup = types.ReplyKeyboardRemove())

		await DialogState.spanking.set()
		await state.set_data({'componion': componion[0]})

		state_ = dp.current_state(chat=componion[0], user=componion[0])
		await state_.set_state(DialogState.spanking)
		await state_.set_data({'componion': chat_id})

		db.delete({'table': 'wait_list', 'user_id': chat_id})
		db.delete({'table': 'wait_list', 'user_id': componion[0]})



#Пересылка текстовых сообщений
async def spenking_now_text(msg: types.Message, state: FSMContext):
	comp_id = await state.get_data()
	comp_id = comp_id['componion']

	send_text = msg.text
	await bot.send_message(comp_id, send_text)


#Пересылка фото
async def spenking_now_photo(msg: types.Message, state: FSMContext):
	comp_id = await state.get_data()
	comp_id = comp_id['componion']

	file_id = msg.photo.file_id
	await bot.send_photo(comp_id, file_id)


#Пересылка стикеров
async def spenking_now_sticker(msg: types.Message, state: FSMContext):
	sticker_id = msg.sticker.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']

	await bot.send_sticker(comp_id, sticker_id)


#Пересылка обычных файлов
async def spenking_now_document(msg: types.Message, state: FSMContext):
	file_id = msg.document.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']
	
	await bot.send_document(comp_id, file_id)


#Пересылка видео
async def spenking_now_video(msg: types.Message, state: FSMContext):
	file_id = msg.video.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']
	
	await bot.send_video(comp_id, file_id)


#Пересылка видео в круге
async def spenking_now_video_note(msg: types.Message, state: FSMContext):
	file_id = msg.video_note.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']
	
	await bot.send_video_note(comp_id, file_id)


#Пересылка голосовых
async def spenking_now_voice(msg: types.Message, state: FSMContext):
	file_id = msg.voice.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']
	
	await bot.send_voice(comp_id, file_id)


#Пересылка аудио сообщений
async def spenking_now_audio(msg: types.Message, state: FSMContext):
	file_id = msg.audio.file_id
	comp_id = await state.get_data()
	comp_id = comp_id['componion']
	
	await bot.send_audio(comp_id, file_id)


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(search_companion_func, text = "▶️Начать диалог", state = None)
	dp.register_message_handler(stop_search_func, text = "Отменить поиск", state = None)

	dp.register_message_handler(spenking_now_text, content_types = ["text"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_photo, content_types = ["photo"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_sticker, content_types = ["sticker"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_document, content_types = ["document"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_video, content_types = ["video"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_video_note, content_types = ["video_note"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_voice, content_types = ["voice"], state = DialogState.spanking)
	dp.register_message_handler(spenking_now_audio, content_types = ["audio"], state = DialogState.spanking)

	dp.register_callback_query_handler(set_feedback, lambda c: c.data, state = None)