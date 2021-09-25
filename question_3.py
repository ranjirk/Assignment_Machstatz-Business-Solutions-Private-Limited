import flask, requests, datetime, datetimerange, json
from datetimerange import DateTimeRange
from flask import request

class belt_calculation:
	def __init__(self, start, end):
		self.url_json = "https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json"
		self.start_time, self.end_time, self.key, self.final_list = start, end, [], []
		self.time_range = DateTimeRange(self.start_time, self.end_time)

	def center(self):
		self.json_data = requests.get(self.url_json).json()
		for self.ele in self.json_data :
			self.ele_type = type(self.ele["id"])
			self.key.append( int( "".join( filter( self.ele_type.isdigit, self.ele["id"] ) ) ) )
		self.keys = set(self.key)
		self.dic_data = [(self.x, []) for self.x in self.keys]
		self.pre_dict = dict(self.dic_data)

		for self.element in self.json_data :
			self.cur_time = self.element["time"]+ "Z"
			self.cur_time = self.cur_time.replace(" ", "T")
			if self.cur_time in self.time_range:
				if self.element["state"] :
					self.tmp_belt_1, self.tmp_belt_2 = 0, self.element["belt2"]
				else :
					self.tmp_belt_1, self.tmp_belt_2 = self.element["belt1"], 0
					self.id_type = type(self.element["id"])
					self.id = int( "".join( filter( self.id_type.isdigit, self.element["id"] ) ) )
					self.pre_dict[self.id].append([self.tmp_belt_1, self.tmp_belt_2])

		for self.key_1 in self.pre_dict :
			self.list_1 = self.pre_dict[self.key_1]
			self.tmp_belt1, self.tmp_belt2 = [], []
			if len(self.list_1) > 1 :
				for self.elem in self.list_1:
					self.tmp_belt1.append(self.elem[0])
					self.tmp_belt2.append(self.elem[1])
				self.avg_belt1 = int(sum(self.tmp_belt1)/len(self.tmp_belt1))
				self.avg_belt2 = int(sum(self.tmp_belt2)/len(self.tmp_belt2))
			elif len(self.list_1) == 1 :
				self.avg_belt1 = self.list_1[0][0]
				self.avg_belt2 = self.list_1[0][1]
			else :
				self.avg_belt1 = 0
				self.avg_belt2 = 0
			self.final_list.append( { "id" : self.key_1, "avg_belt1" : self.avg_belt1, "avg_belt1" : self.avg_belt1 } )

		return self.final_list
# _____________________________________________________________________________________________________________________
app = flask.Flask(__name__)

@app.route('/hello')
def hello():
	start_time = request.args.get('start_time', default = '-1', type = str)
	end_time = request.args.get('end_time', default = '-1', type = str)
	obj = belt_calculation(start_time, end_time)
	res = obj.center()
	json_list = json.dumps(res)
	return json_list
app.run(debug=True, host="0.0.0.0", port=8000)