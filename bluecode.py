#!/usr/bin/env python3
#vi: set autoindent noexpandtab tabstop=4 shiftwidth=4


import base64
from configparser import ConfigParser
from enum import StrEnum
import requests
import sys

class Bc:
    url = []
    access_id = []
    access_key = []
    branch = []
    auth = [] # base64 encoded basic auth string

class Bc_magic(StrEnum):
    MAGIC_ALWAYS_SUCCESSFUL = "98802222100100123456"
    MAGIC_ALWAYS_SUCCESSFUL_E2E_ID = "98800000000000000100"
    MAGIC_ALWAYS_SUCCESSFUL_EXTRA = "98800000000000000101"
    MAGIC_ALWAYS_SUCCESSFUL_ACQUIRE = "98800000000000000099"
    MAGIC_ERRORLIMIT_EXCEEDED = "98804444000000402007"
    MAGIC_ERROR_TIMEOUT = "98802222999900315000"

class Exampe_return(StrEnum):
    EX_PAYMENT_APPROVED = ' {"payment":{"acquirer_tx_id":"WN0UT3ZN10YO4QTAB4THV3D99Z","consumer_tip_amount":0,"currency":"EUR","end_to_end_id":null,"merchant_callback_url":null,"merchant_tx_id":"mtx_1568194991","requested_amount":1200,"scheme":"BLUE_CODE","slip_note":"www.bluecode.com","state":"APPROVED","total_amount":1200},"result":"OK"}'
    EX_PAYMENT_ERROR_MERCHANT_TX_ID_NOT_UNIQUE = '{"error_code":"MERCHANT_TX_ID_NOT_UNIQUE","result":"ERROR"}'


def read_config():
    parser = ConfigParser()
    cfgname = 'bluecode.ini'
    if len(sys.argv) > 1:
        cfgname = str(sys.argv[1])
    print('Using config: ' + cfgname)

    parser.read(cfgname)
    Bc.url = parser.get('Bluecode', 'url')
    Bc.access_id = parser.get('Bluecode', 'access_id')
    Bc.access_key = parser.get('Bluecode', 'access_key')
    Bc.branch = parser.get('Bluecode', 'branch')

    auth_str = Bc.access_id + ':' + Bc.access_key
    auth_bytes = auth_str.encode('ascii')
    auth64_bytes = base64.b64encode(auth_bytes)
    auth64 = auth64_bytes.decode('ascii')
    Bc.auth = auth64

def bc_payment():
    url = Bc.url + "/payment"
    payload = {
        "branch_ext_id": "test",
        "merchant_tx_id": "mtx_1568194992",
        "scheme": "AUTO",
       # "token": Bc_magic.MAGIC_ALWAYS_SUCCESSFUL.value,
        "barcode": Bc_magic.MAGIC_ALWAYS_SUCCESSFUL.value,
        "requested_amount": 1200,
        "currency": "EUR",
        "slip": "Thanks for shopping with us!"
    }
    headers = {
        "content-type": "application/json",
        "authorization": 'Basic ' + Bc.auth
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

read_config()
bc_payment()

