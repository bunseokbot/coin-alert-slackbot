from flask import Flask, request, Response, abort

import json
import requests
import yaml

app = Flask(__name__)

APIS = {
    "coinone": "https://api.coinone.co.kr/ticker?currency=all",
    "korbit": {
        "btc": "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=btc_krw",
        "eth": "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=eth_krw",
        "etc": "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=etc_krw",
        "xrp": "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=xrp_krw"
    },
    "bithumb": "https://api.bithumb.com/public/ticker/all",
    "korim": "http://coin.kor.im/json/coin_data.json"
}

config = yaml.load(open('config.yml').read())


def get_kimchiinfo():
    msg = ""

    try:
        data = requests.get(APIS['korim']).json()

        msg += "BTC: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_btc_p']), int(data['polo_btc']), data['coinone_btc'])
        msg += "ETH: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_eth_p']), int(data['polo_eth']), data['coinone_eth'])
        msg += "ETC: {} % ({} KRW, {} KRW)\n".format(int(data['coinone_etc_p']), int(data['polo_etc']), data['coinone_etc'])
        msg += "XRP: {} % ({} KRW, {} KRW)".format(int(data['coinone_xrp_p']), int(data['polo_xrp']), data['coinone_xrp'])
    except:
        msg += "Error while loading premieum info"

    return msg


def get_coinoneinfo():
    msg = ""

    try:
        data = requests.get(APIS['coinone']).json()
        msg += "BTC : {} Won (Volume : {} BTC)\n".format(data['btc']['last'], data['btc']['volume'])
        msg += "ETH : {} Won (Volume : {} ETH)\n".format(data['eth']['last'], data['eth']['volume'])
        msg += "ETC : {} Won (Volume : {} ETC)\n".format(data['etc']['last'], data['etc']['volume'])
        msg += "XRP : {} Won (Volume : {} XRP)".format(data['xrp']['last'], data['xrp']['volume'])

    except:
        msg += "Error while loading coinone exchange info"

    return msg


def get_korbitinfo():
    msg = ""

    try:
        for coin in APIS['korbit'].keys():
            data = requests.get(APIS['korbit'][coin]).json()
            msg += "{} : {} Won (Volume : {} {})\n".format(coin.upper(), data['last'], data['volume'], coin.upper())
        msg = msg[:-1]
    except:
        msg += "Error while loading korbit exchange info"

    return msg


def get_bithumbinfo():
    msg = ""

    try:
        data = requests.get(APIS['bithumb']).json()['data']
        msg += "BTC : {} Won (Volume : {} BTC)\n".format(data['BTC']['buy_price'], data['BTC']['units_traded'])
        msg += "ETH : {} Won (Volume : {} ETH)\n".format(data['ETH']['buy_price'], data['ETH']['units_traded'])
        msg += "ETC : {} Won (Volume : {} ETC)\n".format(data['ETC']['buy_price'], data['ETC']['units_traded'])
        msg += "XRP : {} Won (Volume : {} XRP)\n".format(data['XRP']['buy_price'], data['XRP']['units_traded'])
        msg += "LTC : {} Won (Volume : {} LTC)\n".format(data['LTC']['buy_price'], data['LTC']['units_traded'])
        msg += "DASH : {} Won (Volume : {} DASH)\n".format(data['DASH']['buy_price'], data['DASH']['units_traded'])

    except:
        msg += "Error while loading bithumb exchange info"

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

@app.route("/coinone", methods=["POST"])
def coinone():
    if request.form.get('token') == config['token']:
        coinmsg = get_coinoneinfo()

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


@app.route("/korbit", methods=["POST"])
def korbit():
    if request.form.get('token') == config['token']:
        coinmsg = get_korbitinfo()

        response = {
            'response_type': 'in_channel',
            'text': 'Current korbit market status',
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


@app.route("/bithumb", methods=["POST"])
def bithumb():
    if request.form.get('token') == config['token']:
        coinmsg = get_bithumbinfo()

        response = {
            'response_type': 'in_channel',
            'text': 'Current bithumb market status',
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
