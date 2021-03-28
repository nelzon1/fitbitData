from flask import Flask,request,jsonify
from sqlalchemy import create_engine
import json
import datetime

app = Flask(__name__)
dbeng = -1 #init global db engine
dbconn = -1
ENV = {}

with open('init.json','r') as json_file:
	ENV = json.load(json_file)

'''
need methods for:
Send a happiness update - DONE
Send a weight update  - DONE
Get last 3 months of data for:
	steps
	weight
	sleep score
	happiness
	
'''

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def initializeDB(dbeng):
	#try:
	dbeng = create_engine(ENV['MYSQL_ADDRESS'].format(ENV['MYSQL_USER'],
														ENV['MYSQL_PW'],
														ENV['MYSQL_PORT'],
														ENV['MYSQL_DB']))
	return dbeng.connect()
	'''
	except:
		dbeng = -1
		return dbeng
	'''
dbconn = initializeDB(dbeng)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/auth')
def hello_world():
	return "Thank you for logging into JNelson's fitbit data app! \n You may close your browser";

@app.route('/mood/send/',methods=['POST'])
def sendMood():
	try:
		if 'val' in request.args:

			value = float(request.args['val'])
			if value < 1 or value > 100:
				raise ValueError('Value must be between 1 and 100')
			datestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			dbconn.execute(f"INSERT INTO MOOD (mood,datetime) VALUES({value},'{datestr}')")

			return 'Thanks for sending val=' + str(value)

		else:
			raise InvalidUsage('Missing value in URL', status_code=400)

	except ValueError:
		raise InvalidUsage('Invalid value. Must be 0 - 100', status_code=400)

	return 0

@app.route('/weight/send/',methods=['POST'])
def sendWeight():
	try:
		if 'val' in request.args:

			value = float(request.args['val'])
			if value < 1 or value > 300:
				raise ValueError('Value must be between 1 and 100')
			datestr = datetime.datetime.today().strftime('%Y-%m-%d')
			dbconn.execute(f"INSERT INTO WEIGHT (weight,date) VALUES({value},'{datestr}')")

			return 'Thanks for sending val=' + str(value)

		else:
			raise InvalidUsage('Missing value in URL', status_code=400)

	except ValueError:
		raise InvalidUsage('Invalid value. Must be 1 - 300', status_code=400)

	return 0