import requests
import hashlib
import json
import os
import math
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('ACCESS_TOKEN')

url = 'https://hackattic.com'

problem_r = requests.get(
    url + f"/challenges/mini_miner/problem?access_token={token}"
)

problem = problem_r.json()

difficulty = problem['difficulty']
block = problem['block']

nonce = -1
expected = '0' * math.ceil(difficulty/4)
while True:
    nonce += 1
    block['nonce'] = nonce
    sha256 = hashlib.new('sha256')
    block_json = json.dumps(block, sort_keys=True, separators=(',',':'))
    sha256.update(block_json.encode())
    if sha256.hexdigest().startswith(expected):
        break

payload = {}
payload['nonce'] = nonce

solution = requests.post(
    url + f"/challenges/mini_miner/solve?access_token={token}",
    json=payload
)

print(solution.json())
