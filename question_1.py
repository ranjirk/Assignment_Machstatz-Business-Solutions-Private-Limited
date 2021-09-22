import flask, requests
from flask import request
# "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json"

class productivity:
	def __init__(self):
		self.url_json = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json"
		self.key1 = ["year","month","day","hour","minute","second"]
		self.start_val, self.end_val, self.cur_val 	= dict.fromkeys(self.key1), dict.fromkeys(self.key1), dict.fromkeys(self.key1)
		self.shiftA, self.shiftB, self.shiftC = {}, {}, {}
		for self.key2 in ["production_A_count","production_B_count"]:
			self.shiftA["production_A_count"], self.shiftB["production_A_count"], self.shiftC["production_A_count"] = 0, 0, 0
			self.shiftA["production_B_count"], self.shiftB["production_B_count"], self.shiftC["production_B_count"] = 0, 0, 0
		self.shift = { "shiftA" : self.shiftA, "shiftB" : self.shiftB, "shiftC" : self.shiftC }

	def center(self, start, end):
		self.start_time, self.end_time = start, end
		self.start_val["year"], self.start_val["month"], self.start_val["day"], \
		self.start_val["hour"], self.start_val["minute"], self.start_val["second"] = self.time_split(self.start_time, True)
		self.end_val["year"], self.end_val["month"], self.end_val["day"], \
		self.end_val["hour"], self.end_val["minute"], self.end_val["second"] = self.time_split(self.end_time, True)
		self.result = self.production_unit_calc()
		return self.result

	def production_unit_calc(self):
		self.json_data = requests.get(self.url_json).json()
		for self.element in self.json_data :

			 if(self.inTime(self.element["time"])):
			 	self.c_shift = self.shift_calc(self.element["time"])

			 	if self.element["production_A"]:
			 		self.shift[self.c_shift]["production_A_count"] += 1
			 	if self.element["production_B"]:
			 		self.shift[self.c_shift]["production_B_count"] += 1
		return self.shift

	def shift_calc(self, shift_time):
		self.shift_time = shift_time
		self.shift_hour, self.shift_minute, self.shift_second = self.time_split(self.shift_time, False)
		if 6 <= int(self.shift_hour) < 14 :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second) :
					return "shiftA"
		if 14 <= int(self.shift_hour) < 20 :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second) :
					return "shiftB"
		if (20 <= int(self.shift_hour)) or (int(self.shift_hour)<6) :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second) :
					return "shiftC"
# _____________________________________________________________________________________________________________________
	def inTime(self, cur_time):
		self.cur_time, self.bound = cur_time, False
		self.cur_val["year"], self.cur_val["month"], self.cur_val["day"], \
		self.cur_val["hour"], self.cur_val["minute"], self.cur_val["second"] = self.time_split(self.cur_time, True)
		if int(self.start_val["year"]) <= int(self.cur_val["year"]) <= int(self.end_val["year"]):
			if int(self.start_val["month"]) <= int(self.cur_val["month"]) <= int(self.end_val["month"]):
				if int(self.start_val["day"]) <= int(self.cur_val["day"]) <= int(self.end_val["day"]):
					if int(self.start_val["hour"]) <= int(self.cur_val["hour"]) <= int(self.end_val["hour"]):
						if int(self.start_val["minute"]) <= int(self.cur_val["minute"]) <= int(self.end_val["minute"]):
							if int(self.start_val["second"][:-1]) <= int(self.cur_val["second"]) <= int(self.end_val["second"][:-1]):
								return True
		else :
			return False

	def time_split(self, dateTime_string, full_flag):
		if "T" in dateTime_string :
			self.date, self.time = dateTime_string.split("T")
		elif " " in dateTime_string :
			self.date, self.time = dateTime_string.split(" ")
		if full_flag :
			self.year, self.month, self.day = self.date.split("-")
			self.hour, self.minute, self.second = self.time.split(":")
			return self.year, self.month, self.day, self.hour, self.minute, self.second[:-1]
		else :
			self.hour, self.minute, self.second = self.time.split(":")
			return self.hour, self.minute, self.second
# _____________________________________________________________________________________________________________________
app = flask.Flask(__name__)

@app.route('/hello')
def hello():
	start_time = request.args.get('start_time', default = '-1', type = str)
	end_time = request.args.get('end_time', default = '-1', type = str)
	obj = productivity()
	res = obj.center(start_time, end_time)
	return res
app.run(debug=True, host="0.0.0.0", port=8000)
#  http://192.168.1.3:8000/hello