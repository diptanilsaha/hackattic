import requests
import os
import psycopg2
import gzip
from dotenv import load_dotenv
import base64

load_dotenv()

token = os.getenv('ACCESS_TOKEN')

url = 'https://hackattic.com'

problem_r = requests.get(
    url + f"/challenges/backup_restore/problem?access_token={token}"
)

problem = problem_r.json()

with open('dump.sql', 'w') as f:
    f.write(gzip.decompress(base64.b64decode(problem['dump'])).decode('utf-8'))


os.system("sudo -u postgres psql dump < 'dump.sql'")

conn = psycopg2.connect(
    database="dump",
    host="localhost",
    user="h_user",
    password="password",
    port='5432'
)

cursor = conn.cursor()

cursor.execute("select ssn from criminal_records where status='alive';")
alive = cursor.fetchall()
payload = {}
payload['alive_ssns'] = []
for i in alive:
    payload['alive_ssns'].append(i[0])

solution = requests.post(
    url + f"/challenges/backup_restore/solve?access_token={token}",
    json=payload
)

print(solution.json())
