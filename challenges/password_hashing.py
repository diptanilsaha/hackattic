import hashlib
import hmac
import base64
import os
import requests
import scrypt
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('ACCESS_TOKEN')

url = 'https://hackattic.com'

problem_r = requests.get(
    url + f"/challenges/password_hashing/problem?access_token={token}"
)

problem = problem_r.json()

salt = base64.b64decode(problem['salt'])

payload = {}

password = problem['password'].encode('utf-8')

sha256 = hashlib.sha256(password)
hmac_sha256 = hmac.new(key=salt, msg=password, digestmod=hashlib.sha256)

pbkdf2 = hashlib.pbkdf2_hmac(problem['pbkdf2']['hash'], password, salt, problem['pbkdf2']['rounds'])

scrypt_val = scrypt.hash(
    password=password,
    salt=salt,
    N=problem['scrypt']['N'],
    r=problem['scrypt']['r'],
    p=problem['scrypt']['p'],
    buflen=problem['scrypt']['buflen']
)

payload['sha256'] = sha256.hexdigest()
payload['hmac'] = hmac_sha256.hexdigest()
payload['pbkdf2'] = pbkdf2.hex()
payload['scrypt'] = scrypt_val.hex()

solution = requests.post(url + f"/challenges/password_hashing/solve?access_token={token}", json=payload)

print(solution.json())
