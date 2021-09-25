import flask, requests, datetime, datetimerange
from flask import request
from datetimerange import DateTimeRange

class productivity:
	def __init__(self, start, end):
		self.url_json = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json"
		self.start_time, self.end_time, self.shiftA, self.shiftB, self.shiftC = start, end, {}, {}, {}
		self.time_range = DateTimeRange(self.start_time, self.end_time)

		for self.key2 in ["production_A_count","production_B_count"]:
			self.shiftA["production_A_count"], self.shiftB["production_A_count"], self.shiftC["production_A_count"] = 0, 0, 0
			self.shiftA["production_B_count"], self.shiftB["production_B_count"], self.shiftC["production_B_count"] = 0, 0, 0
		self.shift = { "shiftA" : self.shiftA, "shiftB" : self.shiftB, "shiftC" : self.shiftC }

	def center(self):
		self.json_data = requests.get(self.url_json).json()
		for self.element in self.json_data :
			self.cur_time = self.element["time"] + "Z"
			self.cur_time = self.cur_time.replace(" ", "T")
			if self.cur_time in self.time_range:
			 	self.c_shift = self.shift_calc(self.element["time"])
			 	if self.element["production_A"]:
			 		self.shift[self.c_shift]["production_A_count"] += 1
			 	if self.element["production_B"]:
			 		self.shift[self.c_shift]["production_B_count"] += 1
		return self.shift

	def shift_calc(self, shift_time):
		self.shift_time = shift_time
		self.date, self.time = self.shift_time.split(" ")
		self.shift_hour, self.shift_minute, self.shift_second = self.time.split(":")

		if 6 <= int(self.shift_hour) < 14 :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second[:-1]) :
					return "shiftA"
		if 14 <= int(self.shift_hour) < 20 :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second[:-1]) :
					return "shiftB"
		if (20 <= int(self.shift_hour)) or (int(self.shift_hour)<6) :
			if 0 <= int(self.shift_minute) :
				if 0 <= int(self.shift_second[:-1]) :
					return "shiftC"
# _____________________________________________________________________________________________________________________
app = flask.Flask(__name__)

@app.route('/hello')
def hello():
	start_time = request.args.get('start_time', default = '-1', type = str)
	end_time = request.args.get('end_time', default = '-1', type = str)
	obj = productivity(start_time, end_time)
	res = obj.center()
	return res
app.run(debug=True, host="0.0.0.0", port=8000)