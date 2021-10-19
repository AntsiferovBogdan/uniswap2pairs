import json
import os
from factory import abi, address
from tqdm import tqdm
from web3 import Web3, HTTPProvider


def connect():
    url = os.environ["URL"]
    web3 = Web3(HTTPProvider(url))
    print(f'Connection - {web3.isConnected()}')
    contract = web3.eth.contract(address=address, abi=abi)
    return web3, contract


def get_pairs():
    web3, contract = connect()
    start = 10_000_835  # first block in uniswap 2
    stop = web3.eth.block_number
    step = 50_000
    pairs = {}
    for block in tqdm(range(start, stop, step)):
        events = contract.events.PairCreated.createFilter(
            fromBlock=block, toBlock=block + step
            ).get_all_entries()
        for e in events:
            e = e['args']
            pairs[e['pair']] = (e['token0'], e['token1'])
    return for_json('w', pairs)


def for_json(data):
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, 'all_pairs.json')
    with open(path, 'w', encoding='utf-8') as f:
        return f.write(json.dumps(data))


if __name__ == '__main__':
    get_pairs()
    print('ready!')
