#!/usr/bin/env python3

import psycopg2
import binascii
import bitcoin
import requests

conn = psycopg2.connect("dbname='mywill_btc' user='mywill_btc' host='localhost' password='mywill_btc'")
cur = conn.cursor()

while 1:
    try:
        btc_priv = input()
    except EOFError:
        break
    btc_pub = bitcoin.privtopub(btc_priv)
    btc_addr = bitcoin.pubtoaddr(btc_pub)
    cur.execute("INSERT INTO btc_accounts (btc_addr, used, eth_addr, btc_balance) VALUES ('{btc_addr}', false, '', 0);".format(btc_addr=btc_addr))
    r = requests.post(
            'http://user:password@127.0.0.1:8332/',
            json={'method': 'importaddress', 'params': [btc_addr, btc_addr, False], 'id': 1, 'jsonrpc': '1.0'}
    )    
    print(r.content)

conn.commit()
cur.close()
conn.close()
