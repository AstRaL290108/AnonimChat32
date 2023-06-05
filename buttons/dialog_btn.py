from aiogram import types

close = types.ReplyKeyboardMarkup(resize_keyboard = True)
btn1 = types.KeyboardButton("Отменить поиск")
close.add(btn1)