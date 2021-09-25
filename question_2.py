import flask, requests, datetime, datetimerange
from flask import request
from datetimerange import DateTimeRange

class productivity:
	def __init__(self, start, end):
		self.start_time, self.end_time, self.runtimes, self.downtimes = start, end, 0, 0
		self.time_range = DateTimeRange(self.start_time, self.end_time)
		self.url_json = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json"

	def center(self):
		self.json_data = requests.get(self.url_json).json()
		for self.element in self.json_data :
			self.cur_time = self.element["time"] + "Z"
			self.cur_time = self.cur_time.replace(" ", "T")
			if self.cur_time in self.time_range:
			 	if self.element["runtime"] > 1021 :
			 		self.down = self.element["runtime"] - 1021
			 		self.run  = 1021
			 	else :
			 		self.run  = self.element["runtime"]
			 		self.down = self.element["downtime"]
			 	self.runtimes  += self.run
			 	self.downtimes += self.down
			 	
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
app = flask.Flask(__name__)

@app.route('/hello')
def hello():
	start_time = request.args.get('start_time', default = '-1', type = str)
	end_time = request.args.get('end_time', default = '-1', type = str)
	obj = productivity(start_time, end_time)
	res = obj.center()
	return res
app.run(debug=True, host="0.0.0.0", port=8000)