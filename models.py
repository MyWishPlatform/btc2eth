from app import db
from sqlalchemy.dialects.postgresql import JSON


class BTCAccount(db.Model):
    __tablename__ = 'btc_accounts'

    id = db.Column(db.Integer, primary_key=True)
    btc_addr = db.Column(db.String())
    eth_addr = db.Column(db.String())
    used = db.Column(db.Boolean())
    btc_balance = db.Column(db.Numeric(20,0))
#    eth_transactions = db.relationship('ETHTransaction', backref='BTCAccount', lazy=True)

'''
class ETHTransaction(db.Model):
    __tablename__ = 'eth_transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    old_btc_balance = db.Column(db.Numeric(20,0))
    new_btc_balance = db.Column(db.Numeric(20,0))
    eth_value = db.Column(db.Numeric())
    btc_account_id = db.Column(db.Integer, db.ForeignKey('BTCAccount.id'), nullable=False)
'''
