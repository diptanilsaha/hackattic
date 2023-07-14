import requests
import os
import subprocess
from dotenv import load_dotenv
import base64

load_dotenv()

token = os.getenv('ACCESS_TOKEN')

url = 'https://hackattic.com'

problem_r = requests.get(
    url + f"/challenges/tales_of_ssl/problem?access_token={token}"
)

problem = problem_r.json()

private_key = problem['private_key']

country = problem['required_data']['country']
domain = problem['required_data']['domain']
country_code = ''.join([i[0] for i in country.split(' ')])

with open('domain.key', 'w') as f:
    f.write('-----BEGIN RSA PRIVATE KEY-----\n')
    f.write(private_key)
    f.write('\n-----END RSA PRIVATE KEY-----\n')

cmd = f"openssl req -x509 -key domain.key -set_serial {problem['required_data']['serial_number']} -subj '/C={country_code}/CN={domain}/ST={country}' -out cert.pem"

with open('cert.sh', 'w') as f:
    f.write(cmd)

directory = os.path.dirname(os.path.realpath(__file__))

subprocess.run('sh cert.sh', shell=True)

cmd = "openssl x509 -outform der -in cert.pem -out cert.der"

with open('der.sh', 'w') as f:
    f.write(cmd)

subprocess.run('sh der.sh', shell=True)


with open('cert.der', 'rb') as f:
    content = f.read()

payload = {}
payload['certificate'] = base64.b64encode(content).decode('utf-8')

solution = requests.post(
    url + f"/challenges/tales_of_ssl/solve?access_token={token}",
    json=payload
)

print(solution.json())
