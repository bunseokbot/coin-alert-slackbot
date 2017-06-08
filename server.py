from flask import Flask, request, Response, abort

import json
import requests
import yaml

app = Flask(__name__)

APIS = {
    "coinone": "https://api.coinone.co.kr/ticker?currency=all"
}

config = yaml.load(open('config.yml').read())


def get_coininfo():
    msg = ""

    try:
        data = requests.get(APIS['coinone']).json()
        msg += "BTC : {} Won (Volume : {} BTC)\n".format(data['btc']['last'], data['btc']['volume'])
        msg += "ETH : {} Won (Volume : {} ETH)\n".format(data['eth']['last'], data['eth']['volume'])
        msg += "ETC : {} Won (Volume : {} ETC)\n".format(data['etc']['last'], data['etc']['volume'])
        msg += "XRP : {} Won (Volume : {} XRP)".format(data['xrp']['last'], data['xrp']['volume'])
    except:
        msg += "Error while loading currency info"

    return msg


@app.route("/")
def hello():
    return 'hello?'


@app.route("/coin", methods=["POST"])
def coin():
    if request.form.get('token') == config['token']:
        coinmsg = get_coininfo()

        response = {
            'response_type': 'in_channel',
            'text': 'Current coinone market status',
            'attachments': [
                {
                    'text': coinmsg
                }
            ]
        }

        return Response(
            json.dumps(response),
            status=200,
            mimetype="application/json"
        )
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True)
