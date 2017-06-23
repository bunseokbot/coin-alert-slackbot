from flask import Flask, request, Response, abort

import json
import requests
import yaml

app = Flask(__name__)

APIS = {
    "coinone": "https://api.coinone.co.kr/ticker?currency=all",
    "korim": "http://coin.kor.im/json/coin_data.json"
}

config = yaml.load(open('config.yml').read())


def get_kimchiinfo():
    msg = ""

    try:
        data = requests.get(APIS['korim']).json()

        msg += "BTC: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_btc_p']), data['polo_btc'], data['coinone_btc'])
        msg += "ETH: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_eth_p']), data['polo_eth'], data['coinone_eth'])
        msg += "ETC: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_etc_p']), data['polo_etc'], data['coinone_etc'])
        msg += "XRP: {} % ({} KRW, {} KRW)".format(int(data['coinone_xrp_p']), data['polo_xrp'], data['coinone_xrp'])
    except:
        msg += "Error while loading premieum info"

    return msg


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


@app.route("/kimchi", methods=["POST"])
def kimchi():
    if request.form.get('token') == config['token']:
        kimchimsg = get_kimchiinfo()

        response = {
            'response_type': 'in_channel',
            'text': 'Poloniex vs Coinone Premieum status',
            'attachments': [
                {
                    'text': kimchimsg
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
