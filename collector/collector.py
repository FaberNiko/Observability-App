import psutil
import time
import csv
import os
from datetime import datetime, timezone


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "data")
OUT_FILE = os.path.join(OUT_DIR, 'metrics.csv')
INTERVAL = 2

os.makedirs(OUT_DIR, exist_ok=True)


def file_has_header(path):
    return os.path.exists(path) and os.path.getsize(path) > 0


def write_header_if_needed(path):
    if not file_has_header(path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['ts | ' 'iso_time | ' 'cpu | ' 'ram_percent | ' 'disk_percent | ' 'net_sent_delta | ' 'net_recv_delta | ' 'top_proc_1 | ' 'top_proc_1_cpu | ' 'top_proc_2 | ' 'top_proc_2_cpu | ' 'top_proc_3 | ' 'top_proc_3_cpu | '])


def get_top_process(n=3):
    procs = []
    for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent"]):
        try:
            info = p.info
            procs.append(
                (info.get("name") or f"pid:{info.get('pid')}", info.get("cpu_percent") or 0.0))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x[1], reverse=True)

    result = []

    for i in range(n):
        if i < len(procs):
            result.extend([procs[i][0], procs[i][1]])
        else:
            result.extend(["", 0.0])
    return result


def main():
    write_header_if_needed(OUT_FILE)
    prev_net = psutil.net_io_counters()
    print("Collector has started. Pres CTRL+C to stop.")

    try:
        while True:

            ts = int(time.time())
            iso = datetime.now(timezone.utc).isoformat().replace(' +00:00 ',' Z ')
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            net = psutil.net_io_counters()
            net_sent_delta = net.bytes_sent - prev_net.bytes_sent
            net_recv_delta = net.bytes_recv - prev_net.bytes_recv
            prev_net = net

            top = get_top_process(3)

            print(
                f"[{iso}] | CPU: {cpu}% | RAM: {ram}% | DISK: {disk}% | NET+= {net_sent_delta} | NET-= {net_recv_delta}")
            print(
                f"Top: {top[0]}({top[1]}%), {top[2]}({top[3]}%), {top[4]}({top[5]}%)")

            with open(OUT_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                row = [ts, iso, cpu, ram, disk,
                       net_sent_delta, net_recv_delta] + top
                writer.writerow(row)

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("Collector stopped by user")
    except Exception as e:
        print("Collector error ", e)


if __name__ == "__main__":
    main()
