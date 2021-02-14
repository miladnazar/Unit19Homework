import subprocess
import json
import bit
import web3

import os
import constant


mnemonic = os.getenv("MNEMONIC", "donor episode angle divide modify vendor crunch argue vacuum poverty nature balance")

def derive_wallets(mnemonic):
    output_json = dict()
    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=eth", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['eth'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc'] = command_out

    command = ["/Users/miladnazar/Desktop/Homework/Unit19Homework/Starter-Code/hd-wallet-derive/hd-wallet-derive.php", "-g", "--mnemonic='"+mnemonic+"'", "--cols=path,address,privkey,pubkey", "--format=json", "--coin=btc-test", "--numderive=3"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    command_out = json.loads(stdout)

    output_json['btc-test'] = command_out

    return output_json

def priv_key_to_account(privkey, coin):
    if coin == constant.BTCTEST:
        return bit.PrivateKeyTestNet(privkey)
    
    elif coin == constant.ETH:
        return web3.eth.accounts.privateKeyToAccount(privkey)



if __name__ == "__main__":
    coins = derive_wallets(mnemonic)
    print(coins)
    print(coins['eth'][0]['privkey'])
    print(priv_key_to_account('0xe4be1f8b03f60e7563fa45a52025fb117aff24a5ec1b9b63d16b0fc88fa0645a', 'eth'))
