import subprocess
import json
import bit
import web3
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
#from eth_account import Account

import os
import constant

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#accounts = Account.from_key(os.getenv("0xe631cb477215f7510c5f5dc8bc0b32ee9c8b1c43dd34b44607b6037d388c93d3"))
mnemonic = os.getenv("MNEMONIC", "donor episode angle divide modify vendor crunch argue vacuum poverty nature balance")

def derive_wallets(mnemonic):
    output_json = dict()
    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=eth", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['eth'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc-test", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc-test'] = command_out

    return output_json


def priv_key_to_account(privkey, coin):
    if coin == constant.BTCTEST:
        return bit.PrivateKeyTestnet(privkey)
    
    elif coin == constant.ETH:
        return web3.eth.accounts.privateKeyToAccount(privkey)

def create_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()


if __name__ == "__main__":
    coins = derive_wallets(mnemonic)
    print(coins)
    print(coins['eth'][0]['privkey'])

