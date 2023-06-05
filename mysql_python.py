import pymysql
import datetime

class DataBase:
	def __init__(self, user, password, host, database):
		self.db = pymysql.connect(
				user = user,
				password = password,
				host = host,
				database = database
			)
		self.cur = self.db.cursor()



	def insert_into(self, dict_):
		self.db.ping(reconnect = True)
		table = dict_['table']
		dict_.pop('table')
		keys = list(dict_.keys())

		request = f"INSERT INTO `{table}` ("

		for i in keys:
			if i == keys[-1]:
				request += f"{i}) "
			else:
				request += f"{i}, "

		request += "VALUES ("

		for i in keys:
			if i == keys[-1]:
				if isinstance(dict_[i], str):
					request += f"'{dict_[i]}')"
				elif isinstance(dict_[i], datetime.date) or isinstance(dict_[i], datetime.datetime):
					request += f"'{str(dict_[i])}')"
				else:
					request += f"{dict_[i]})"
			else:
				if isinstance(dict_[i], str):
					request += f"'{dict_[i]}', "
				elif isinstance(dict_[i], datetime.date) or isinstance(dict_[i], datetime.datetime):
					request += f"'{str(dict_[i])}', "
				else:
					request += f"{dict_[i]}, "

		self.cur.execute(request)
		self.db.commit()


	def delete(self, dict_):
		self.db.ping(reconnect = True)
		table = dict_['table']
		dict_.pop('table')
		keys = list(dict_.keys())

		if isinstance(dict_[keys[0]], str):
			request = f"DELETE FROM `{table}` WHERE {keys[0]} = '{dict_[keys[0]]}'"
		elif isinstance(dict_[keys[0]], datetime.date) or isinstance(dict_[keys[0]], datetime.datetime):
			request = f"DELETE FROM `{table}` WHERE {keys[0]} = '{str(dict_[keys[0]])}'"
		else:
			request = f"DELETE FROM `{table}` WHERE {keys[0]} = {dict_[keys[0]]}"

		self.cur.execute(request)
		self.db.commit()


	def select(self, dict_):
		self.db.ping(reconnect = True)
		table = dict_['table']
		dict_.pop('table')
		types = dict_['type']
		dict_.pop('type')

		if types == "all":
			request = f"SELECT * FROM `{table}`"
			self.cur.execute(request)
			self.db.commit()

			resp = self.cur.fetchall()
			return resp

		else:
			keys = list(dict_.keys())

			if isinstance(dict_[keys[0]], str):
				request = f"SELECT * FROM `{table}` WHERE {keys[0]} = '{dict_[keys[0]]}'"
			elif isinstance(dict_[keys[0]], datetime.date) or isinstance(dict_[keys[0]], datetime.datetime):
				request = f"SELECT * FROM `{table}` WHERE {keys[0]} = '{str(dict_[keys[0]])}'"
			else:
				request = f"SELECT * FROM `{table}` WHERE {keys[0]} = {dict_[keys[0]]}"

			self.cur.execute(request)
			self.db.commit()

			if types == "one":
				resp = self.cur.fetchone()
			elif types == "many":
				resp = self.cur.fetchall()
				if str(resp) == "()":
					resp = None

			return resp


	def update(self, dict_):
		colamns = dict_['colamns']
		colamn_keys = list(colamns.keys())

		where = dict_['where']
		where_keys = list(where.keys())

		table = dict_['table']

		request = f"UPDATE `{table}` SET "
		for i in colamn_keys:
			if colamn_keys[-1] == i:
				if isinstance(colamns[i], str):
					request += f"{i} = '{colamns[i]}' "
				elif isinstance(colamns[i], datetime.date) or isinstance(colamns[i], datetime.datetime):
					request += f"{i} = '{str(colamns[i])}' "
				else:
					request += f"{i} = {colamns[i]} "
			else:
				if isinstance(colamns[i], str):
					request += f"{i} = '{colamns[i]}', "
				elif isinstance(colamns[i], datetime.date) or isinstance(colamns[i], datetime.datetime):
					request += f"{i} = '{str(colamns[i])}', "
				else:
					request += f"{i} = {colamns[i]}, "

		if isinstance(where[where_keys[0]], str):
			request += f"WHERE {where_keys[0]} = '{where[where_keys[0]]}'"
		elif isinstance(where[where_keys[0]], datetime.date) or isinstance(colamns[i], datetime.datetime):
			request += f"WHERE {where_keys[0]} = '{str(where[where_keys[0]])}'"
		else:
			request += f"WHERE {where_keys[0]} = {where[where_keys[0]]}"


		self.cur.execute(request)
		self.db.commit()