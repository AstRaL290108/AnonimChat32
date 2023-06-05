from aiogram import types

main_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
btn1 = types.KeyboardButton("▶️Начать диалог")
#btn2 = types.KeyboardButton("🔮Привелегии")
btn3 = types.KeyboardButton("👤Профиль")
btn4 = types.KeyboardButton("☎️Наши контакты")
btn5 = types.KeyboardButton("🚪Комнаты")
main_menu.add(btn1)
main_menu.add(btn5, btn3)
main_menu.add(btn4)

profile_menu = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton(text = "📝Изменить профиль", callback_data = "let_change")
profile_menu.add(btn)


our_contacts = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text = "Канал YouTube", url = "https://www.youtube.com/@underground1094")
btn2 = types.InlineKeyboardButton(text = "Канал Telegram", url = "https://t.me/underground_web")
btn3 = types.InlineKeyboardButton(text = "Паблик в ВК", url = "https://vk.com/public219159319")
btn4 = types.InlineKeyboardButton(text = "Сайт UnderGround", url = "https://underground.pythonanywhere.com")
our_contacts.add(btn1)
our_contacts.add(btn2)
our_contacts.add(btn3)
our_contacts.add(btn4)