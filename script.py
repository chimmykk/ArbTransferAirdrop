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

# Read contract ABI from file
with open('abi.json', 'r') as f:
    contract_abi = json.load(f)

def send(provider, key, reciever):
    print(key)
    print(reciever)
    acct = Account.from_key(key)
    contract_address = '0x912CE59144191C1204E64559FE8253a0e49E6548'
    token_contract = provider.eth.contract(address=contract_address, abi=contract_abi)
    token_balance = token_contract.functions.balanceOf(acct.address).call()
    print(token_balance);
    if token_balance > 0:
        nonce = provider.eth.getTransactionCount(acct.address)
        tx = {
            'from': acct.address,
            'chainId': 42161,
            'nonce': nonce,
            'to': contract_address,
            'data': 'a9059cbb' + reciever[2:].rjust(64, '0') + hex(token_balance)[2:].rjust(64, '0'),
            'gas': 1000000,
            'value': provider.toWei(0,'ether'),
            'gasPrice': provider.toWei(0.1, 'gwei')
        }
        signed_tx = provider.eth.account.signTransaction(tx, key)
        provider.eth.sendRawTransaction(signed_tx.rawTransaction)

while True:
    try:
        send(ws_w3, os.environ.get('PRIVATE_KEY'), os.environ.get('SAFE_ADDRESS'))
        send(http_w3, os.environ.get('PRIVATE_KEY'), os.environ.get('SAFE_ADDRESS'))
        time.sleep(60) # Wait 60 seconds before trying again
    except Exception as e:
        print(f"Error transferring tokens: {str(e)}")
