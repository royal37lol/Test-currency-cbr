from flask import Flask, request
from parse_xml_cbr import cache, currency_rate, SymbException
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

curr = cache()

@app.route("/api/v1.0/availabeCurrency")
def get_currency():
    return curr

@app.route("/api/v1.0/get_range", methods=['GET'])
def get_range():
    if ('date_start' in request.args) and ('date_end' in request.args) and \
            ('currency_symbol' in request.args):
        date_start = request.args['date_start']
        date_end = request.args['date_end']
        currency_name = request.args['currency_symbol']
        try:
            currency_rate(date_start, date_end, currency_name)
        except SymbException:
            return f"Invalid currency symbol {currency_name}"
        return currency_rate(date_start, date_end, currency_name)

    else:
        return 'Invalid input'


if __name__ == "__main__":
    app.run(debug=True)
