from aiogram.dispatcher.filters.state import StatesGroup, State

class RegisterState(StatesGroup):
	get_sex = State()
	get_age = State()
	get_country = State()
	get_room = State()


class DialogState(StatesGroup):
	spanking = State()


class ChangeState(StatesGroup):
	get_sex = State()
	get_age = State()
	get_country = State()
	get_room = State()