import random
import json
import os
import requests
from threading import Thread, Semaphore

idx = set()
x = 1
semaphore = Semaphore()

def User():
    global x, idx
    if not os.path.exists("2010.txt"):
        with open("2010.txt", "w") as file:
            pass
    with open("2010.txt", "r") as file:
        lines = file.readlines()
        existing_ids = set(line.split('|')[1].strip() for line in lines if '|' in line)
    
    while True:
        iD = str(random.randrange(1, 1278800))
        if iD not in existing_ids and iD not in idx:
            idx.add(iD)
            lsd = ''.join(random.choice('azertyuiopmlkjhgfdsqwxcvbnAZERTYUIOPMLKJHGFDSQWXCVBN1234567890') for _ in range(32))
            data = {
                "lsd": lsd,
                "variables": json.dumps({"id": iD, "render_surface": "PROFILE"}),
                "doc_id": "25618261841150840"
            }
            try:
                response = requests.post("https://www.instagram.com/api/graphql", headers={"X-FB-LSD": lsd}, data=data)
                if response.status_code == 200:
                    username = response.json().get('data', {}).get('user', {}).get('username')
                    if username:
                        with semaphore:
                            with open("2010.txt", "a") as file:
                                file.write(f"{username}|{iD}\n")
                                print(x, "-", username)
                                existing_ids.add(iD)
                                x += 1
            except:
                continue

for i in range(40):
    Thread(target=User).start()
    
