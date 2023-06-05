from aiogram import types

let_test = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton(text = "➡️Начать тест", callback_data = "let_test")
let_test.add(btn)

choose_sex = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text = "🙍‍♀️Женский", callback_data = "🙍‍♀️Девушка")
btn2 = types.InlineKeyboardButton(text = "🙎‍♂️Мужской", callback_data = "🙎‍♂️Мужчина")
choose_sex.add(btn1, btn2)

select_country = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text = "🇷🇺Россия", callback_data = "🇷🇺Россия")
btn2 = types.InlineKeyboardButton(text = "🇧🇾Беларусь", callback_data = "🇧🇾Беларусь")
btn3 = types.InlineKeyboardButton(text = "🇰🇿Казахстан", callback_data = "🇰🇿Казахстан")
select_country.add(btn1)
select_country.add(btn2)
select_country.add(btn3)