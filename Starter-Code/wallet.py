import subprocess
import json
import bit
import web3
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit.network import NetworkAPI
import os
import constant

load_dotenv()

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

private_key = os.getenv("PRIVATE_KEY")

mnemonic = os.getenv("MNEMONIC", "donor episode angle divide modify vendor crunch argue vacuum poverty nature balance")

def derive_wallets(mnemonic):
    output_json = dict()
    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Wallet/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=eth", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['eth'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Wallet/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Unit19Homework/Wallet/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc-test", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc-test'] = command_out

    return output_json


def priv_key_to_account(coin, private_key):
    if coin == constant.BTCTEST:
        return bit.PrivateKeyTestnet(private_key)
    
    elif coin == constant.ETH:
        return Account.privateKeyToAccount(private_key)
        #Account.from_key(private_key)

def create_tx(coin, account, recipient, amount):
    
    if coin == constant.BTCTEST: # To Ask I changed the btc to btc-test
        return account.create_transaction([(str(recipient),amount,'btc-test')])
        #gasEstimate = w3.eth.estimateGas({"from": account.address, "to": recipient, "value": amount}
    #)
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
def send_tx(coin, account, recipient, amount):
    if coin == constant.BTCTEST:
        print("BTC token")
    elif coin == constant.ETH:
        tx = create_tx('eth', account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    elif coin == constant.BTC_TEST:
        #print("BTC_TEST token")
        tx_hash=create_tx('btc-test',account,recipient,amount)
        result=NetworkAPI.broadcast_tx_testnet(tx_hash)
        return result

if __name__ == "__main__":
    coins = derive_wallets(mnemonic)
    #print(coins)
    #print(coins['eth'][0]['0xbfa2645CDCA00D5915c8cCCd9696E95934d74971'])
    # This is how you get the BTCtest wallet information (Public and Private Keys)
    #tmp = bit.PrivateKeyTestnet()
    #print(tmp.address)
    #print(tmp.to_wif())

    account=priv_key_to_account('btc-test', 'cSS7cx4X6QKULydXKZ4C6jhQxZLnF1NVc7WMTMWme94nsVtn3sVh')
    create_tx('btc-test', account, coins['btc-test'][0]['address'], 0.00001)

    output = send_tx('btc-test', account, coins['btc-test'][0]['address'], 0.00001)
    print(output)
