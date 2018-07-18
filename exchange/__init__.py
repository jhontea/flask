from flask import Flask
from exchange.main.controllers import main
from exchange.rate.controllers import rate

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(rate, url_prefix='/rate')