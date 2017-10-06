#!/usr/bin/env python3

import time
import requests
import json
import psycopg2
import binascii
import rlp
from ethereum import abi
from ethereum import transactions, utils

FROM_PRIV = 'edd277837ffd504ebbe80df0647c86c10f078dc43c8cdb811e6f3ab1e400b55c'
FROM_ADDR = '0x2605dd628e9466136718add604e383b4d7308eb5'
# TOKEN = '0x05C571b3f048C3F8A87C8dcaA5e1434356F9Fdb9'
TOKEN = '0x2298cDfdFa10d44c78B92842A021D3ef9C573e6e'

# ABI = [{"constant":True,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"_name","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"_symbol","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_toExclude","type":"address"}],"name":"addExcluded","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_beneficier","type":"address"},{"name":"_amount","type":"uint256"}],"name":"buyForBitcoin","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"crowdsaleFinished","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"previousOwner","type":"address"},{"indexed":True,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
ABI = [{"constant":True,"inputs":[],"name":"spend","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},             {"constant":False,"inputs":[{"name":"_beneficier","type":"address"},{"name":"_amount","type":"uint256"}],"name":"buyForBitcoin","outputs":[],"payable":        False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"server","outputs":[{"name":"","type":"address"}],"payable":       False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"beneficier","type":"address"},{"indexed":False,        "name":"amount","type":"uint256"}],"name":"Minted","type":"event"}]

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

