#!/usr/bin/env python3

import time
import requests
import json
import psycopg2
import binascii
import rlp
from ethereum import abi
from ethereum import transactions, utils

from settings import *

while 1:
#    try:
        conn = psycopg2.connect("dbname='mywill_btc' user='mywill_btc' host='localhost' password='mywill_btc'")
        cur = conn.cursor()
        cur.execute('select * from btc_accounts where used=True;')
        for acc_id, btc_addr, eth_addr, used, btc_balance in cur.fetchall():
#            try:
                r = requests.post('http://user:password@127.0.0.1:8332/', json={'method': 'getreceivedbyaddress', 'jsonrpc': '1.0', 'id': 1, 'params': [btc_addr, 5]})
                result = json.loads(r.content.decode())['result']
                new_balance = int(result * 10**8)
                print(btc_balance, new_balance)
                if new_balance > btc_balance:
                    delta = int(new_balance - btc_balance)
                    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=ETH')
                    chart = json.loads(response.content.decode())['ETH']
                    wei_amount = int(delta / 10**8 * chart * 10**18)
                    print('wei_amount', wei_amount)
                    nonce = int(json.loads(requests.post('http://127.0.0.1:8545/', json={
                            "method":"parity_nextNonce",
                            "params": [FROM_ADDR],
                            "id":1,
                            "jsonrpc":"2.0"
                    }, headers={'Content-Type': 'application/json'}).content.decode())['result'], 16)
                    print('nonce', nonce)
                    tr = abi.ContractTranslator(ABI)
                    print(eth_addr, wei_amount)
                    data = tr.encode_function_call('buyForBitcoin', [eth_addr, wei_amount])
                    tx = transactions.Transaction(nonce, 20*10**9, 60000, TOKEN, 0, data).sign(FROM_PRIV)
                    raw_tx = binascii.hexlify(rlp.encode(tx)).decode()
                    result = json.loads(requests.post('http://127.0.0.1:8545/', json={
                            "method":"eth_sendRawTransaction",
                            "params": ['0x' + raw_tx],
                            "id":1,
                            "jsonrpc":"2.0"
                    }, headers={'Content-Type': 'application/json'}).content.decode())

                    print(result)

                    cur.execute("update btc_accounts set btc_balance={new_balance} where btc_addr='{btc_addr}';".format(btc_addr=btc_addr, new_balance=new_balance))
                    conn.commit()
                    print('updated')
#            except Exception as e:
#                print(e)
        cur.close()
        conn.close()
#    except Exception as e:
#        print(e)
        time.sleep(10*60)

