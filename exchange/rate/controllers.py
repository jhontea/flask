from flask import Blueprint, Flask, jsonify, request 
from flaskext.mysql import MySQL 
import time

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'funds'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

rate = Blueprint('rate', __name__)

# open connection

conn = mysql.connect()
curr = conn.cursor()

def checkRateExist(fromInput, toInput):
	# get rate id
	query = "SELECT * FROM rate WHERE from_currency ='" + fromInput + "' AND to_currency = '" + toInput + "'"
	return curr.execute(query)


@rate.route('/')
def index():
	try:
		curr.execute('''SELECT * FROM rate_logs''')
		rv = curr.fetchall()

		response = {
			'status': 200,
		    'message': 'Success',
		    'result': rv
		}

		return jsonify(response)
	except Exception as e:
		message = {
	        'status': 200,
	        'message': "Problem executing db: " + str(e)
	    }

		return jsonify(message)

@rate.route('exchange-list')
def getExchangeList():
	try:
		curr.execute('''SELECT 
			from_currency, to_currency, sum(case when created_at=date(now()) then rate end) as rate, avg(rate) as 7_day_avg
		FROM
			funds.rate r
		left JOIN
			funds.rate_logs rl
		ON
			r.id = rl.rate_id and rl.created_at between date_add(date(now()), interval -7 day) and date(now())
		group by
			1,2;''')

		rv = curr.fetchall()

		response = {
			'status': 200,
		    'message': 'Success',
		    'result': rv
		}

		return jsonify(response)
	except Exception as e:
		message = {
	        'status': 200,
	        'message': "Problem executing db: " + str(e)
	    }

		return jsonify(message)


@rate.route('/insert-exchange', methods=['POST'])
def insertExchange():
	# get request from input
	fromInput = request.form.get('from')
	toInput = request.form.get('to')

	if (checkRateExist(fromInput, toInput)):
		try:
			curr.execute('''INSERT INTO rate (`from_currency`, `to_currency`) VALUES (%s, %s)''', (fromInput, toInput))
			conn.commit()

			message = {
		        'status': 200,
		        'message': 'Success'
		    }

			return jsonify(message)
		except Exception as e:
			message = {
		        'status': 500,
		        'message': "Problem inserting into db: " + str(e)
		    }

			return jsonify(message)
	else:
		message = {
	        'status': 500,
	        'message': "Duplicate data"
	    }

		return jsonify(message)


@rate.route('/delete-exchange', methods=['POST'])
def deleteExchange():
	# get request from input
	fromInput = request.form.get('from')
	toInput = request.form.get('to')

	query = "DELETE FROM rate WHERE from_currency ='" + fromInput + "' AND to_currency = '" + toInput + "'"

	try: 
		curr.execute(query)
		conn.commit()

		message = {
	        'status': 200,
	        'message': 'Success'
	    }

		return jsonify(message)

	except Exception as e:
		message = {
	        'status': 500,
	        'message': "Problem deleting into db: " + str(e)
	    }

		return jsonify(message)

@rate.route('/insert-rate', methods=['POST'])
def insertRateLog():
	# get request from input
	fromInput = request.form.get('from')
	toInput = request.form.get('to')
	rate = request.form.get('rate')
	now = time.strftime('%Y-%m-%d %H:%M:%S')

	# get rate id
	query = "SELECT id FROM rate WHERE from_currency ='" + fromInput + "' AND to_currency = '" + toInput + "'"
	curr.execute(query)
	rateId = curr.fetchone() 

	try:
		cur.execute('''INSERT INTO rate_logs (`rate_id`, `rate`, `created_at`) VALUES (%s, %s, %s)''', (rateId[0], rate, now))
		conn.commit()

		message = {
	        'status': 200,
	        'message': 'Success'
	    }

		return jsonify(message)

	except Exception as e:
		message = {
	        'status': 500,
	        'message': "Problem inserting into db: " + str(e)
	    }

		return jsonify(message)
