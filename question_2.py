import flask, requests, datetime
from flask import request

class productivity:
	def __init__(self):
		self.url_json = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json"
		self.key1 = ["year","month","day","hour","minute","second"]
		self.start_val, self.end_val, self.cur_val 	= dict.fromkeys(self.key1), dict.fromkeys(self.key1), dict.fromkeys(self.key1)
		self.runtimes, self.downtimes = 0, 0

	def center(self, start, end):
		self.start_time, self.end_time = start, end
		self.start_val["year"], self.start_val["month"], self.start_val["day"], \
		self.start_val["hour"], self.start_val["minute"], self.start_val["second"] = self.time_split(self.start_time, True)
		self.end_val["year"], self.end_val["month"], self.end_val["day"], \
		self.end_val["hour"], self.end_val["minute"], self.end_val["second"] = self.time_split(self.end_time, True)
		self.production_calc()
		self.result = self.run_down_calc()
		return self.result

	def production_calc(self):
		self.json_data = requests.get(self.url_json).json()
		for self.element in self.json_data :
			 if(self.inTime(self.element["time"])):
			 	if self.element["runtime"] > 1021 :
			 		self.down = self.element["runtime"] - 1021
			 		self.run  = 1021
			 	else :
			 		self.run  = self.element["runtime"]
			 		self.down = self.element["downtime"]
			 	self.runtimes  += self.run
			 	self.downtimes += self.down

	def run_down_calc(self):
		self.run2  = str(datetime.timedelta(seconds = self.runtimes))
		self.down2 = str(datetime.timedelta(seconds = self.downtimes))
		self.r_hrs, self.r_min, self.r_sec = self.run2.split(":")
		self.d_hrs, self.d_min, self.d_sec = self.down2.split(":")
		self.runtime  = self.r_hrs + "h" + self.r_min + "m" + self.r_sec + "s"
		self.downtime = self.d_hrs + "h" + self.d_min + "m" + self.d_sec + "s"
		self.utilization = ( int( self.runtimes ) / ( int( self.runtimes ) + int( self.downtimes ) ) )*100
		self.utilization = round(self.utilization, 2)
		return { "runtime" : self.runtime, "downtime" : self.downtime, "utilization" : self.utilization }
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
			return self.year, self.month, self.day, self.hour, self.minute, self.second
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