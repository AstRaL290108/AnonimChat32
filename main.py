from create_bot import bot, dp
from aiogram.utils import executor

from handlers import *

#https://t.me/anonim_chat32_bot?start=242915
command.register_handlers(dp)
register.register_handlers(dp)
change_profile.register_handlers(dp)
dialog.register_handlers(dp)
menus.register_handlers(dp)

if __name__ == "__main__":
	executor.start_polling(dp)