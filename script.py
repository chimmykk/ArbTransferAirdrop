from web3 import Web3
import time
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
from eth_account import Account
http_provider = Web3.HTTPProvider(os.environ.get('HTTP_RPC'))
http_w3 = Web3(http_provider)
ws_provider = Web3.WebsocketProvider(os.environ.get('WS_RPC'))
ws_w3 = Web3(ws_provider)
#httpfunc()
def http_send(key, reciever):
    print(key)
    print(reciever)
    acct = Account.from_key(key)
    contract_address = '0x912CE59144191C1204E64559FE8253a0e49E6548' #token contract address
    token_contract = http_w3.eth.contract(address=contract_address, abi=contract_abi)
    token_balance = token_contract.functions.balanceOf(acct.address).call()
    print(token_balance);
    if token_balance > 0:
        nonce = http_w3.eth.getTransactionCount(acct.address)
        tx = {
            'from': acct.address,
            'chainId': 42161,
            'nonce': nonce,
            'to': contract_address,
            'data': 'a9059cbb' + reciever[2:].rjust(64, '0') + hex(token_balance)[2:].rjust(64, '0'),
            'gas': 1000000,
            'value': http_w3.toWei(0,'ether'),
            'gasPrice': http_w3.toWei(0.1, 'gwei')
        }
        signed_tx = http_w3.eth.account.signTransaction(tx, key)
        http_w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#Wsfun()
def ws_send(key, reciever):
    print(key)
    print(reciever)
    acct = Account.from_key(key)
    contract_address = '0x912CE59144191C1204E64559FE8253a0e49E6548' #Contract Address
    token_contract = ws_w3.eth.contract(address=contract_address, abi=contract_abi)
    token_balance = token_contract.functions.balanceOf(acct.address).call()
    print(token_balance);
    if token_balance > 0:
        nonce = ws_w3.eth.getTransactionCount(acct.address)
        tx = {
            'from': acct.address,
            'chainId': 42161,
            'nonce': nonce,
            'to': contract_address,
            'data': 'a9059cbb' + reciever[2:].rjust(64, '0') + hex(token_balance)[2:].rjust(64, '0'),
            'gas': 1000000,
            'value': ws_w3.toWei(0,'ether'),
            'gasPrice': ws_w3.toWei(0.1, 'gwei')
        }
        signed_tx = ws_w3.eth.account.signTransaction(tx, key)
        ws_w3.eth.sendRawTransaction(signed_tx.rawTransaction)

while True:
    try:
        ws_send(os.environ.get('PRIVATE_KEY'), os.environ.get('SAFE_ADDRESS')) #try Websocket first
        http_send(os.environ.get('PRIVATE_KEY'), os.environ.get('SAFE_ADDRESS'))

        time.sleep(60) 
    except Exception as e:
        print(f"Error transferring tokens: {str(e)}")
``
