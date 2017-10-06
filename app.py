import binascii
import requests
import rlp
import json
from ethereum import transactions, utils

from flask import Flask, request
from flask_restful import Resource, Api
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mywill_btc:mywill_btc@localhost/mywill_btc'
# app.config['USERNAME'] = 'lastwill_sign'
# app.config['PASSWORD'] = 'lastwill_sign'
db = SQLAlchemy(app)

from models import BTCAccount

class BTC2ETH(Resource):
    def post(self):
        req = request.get_json()
        eth_addr = req['eth_addr']
        try:
            btc_account = db.session.query(BTCAccount).filter(BTCAccount.eth_addr==eth_addr).limit(1).one()
        except:
            btc_account = db.session.query(BTCAccount).filter(BTCAccount.used==False).limit(1).with_for_update().one()
            btc_account.used = True
            btc_account.eth_addr = eth_addr
            db.session.add(btc_account)
            db.session.commit()
        return {'result': btc_account.btc_addr}


api = Api(app)


api.add_resource(BTC2ETH, '/btc_2_eth/')
