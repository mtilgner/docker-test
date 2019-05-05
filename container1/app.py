from flask import Flask, request
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
mongo_uri = 'mongodb://172.17.0.3:27017/stringDB'

mongo = PyMongo(app, uri=mongo_uri)


@app.route('/receive')
def receive_string():

	# send a query string like so:
	# curl "http://localhost:5000/receive?string=foo"
	in_string = request.args.get('string')

	if in_string is not None:
		save_string(in_string)
		return '<h3>string saved: %s</h3>' %(in_string)

	return '<h3>please supply a query string</h3>'

def modify_string(in_string):

	return in_string + 'bar'

def save_string(in_string):

	document = {'original_string': in_string,
                'modified_string': modify_string(in_string),
                'timestamp': datetime.utcnow()}

	mongo.db.strings.insert_one(document)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
