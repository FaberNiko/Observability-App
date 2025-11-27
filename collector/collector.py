import psutil
import time
import csv

with open('metrics.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ts | ' 'cpu | ' 'ram | '])


while True:
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    ts = int(time.time())

    print(f"TS: {ts} | CPU: {cpu}% | RAM: {ram}%")

    with open('metrics.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ts, " " ,cpu, " ", ram])

    time.sleep(1)


