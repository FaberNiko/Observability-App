import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "data")
OUT_FILE = os.path.join(OUT_DIR, 'metrics.csv')

cpu_values = []

try:
    with open(OUT_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
     
        try:
            header = next(reader)
        except StopIteration:
            header = None

        for row in reader:
            if not row or len(row) < 3:
                continue
            raw_cpu = row[2]
            try:
                cpu = float(raw_cpu)
            except ValueError:
                continue
            cpu_values.append(cpu)
except FileNotFoundError:
    print("I can't find file: ", OUT_FILE)
    raise SystemExit(1)

if not cpu_values:
    print("No cpu values found or file is empty")
else:
    max_cpu = max(cpu_values)
    min_cpu = min(cpu_values)
    avg_cpu = sum(cpu_values) / len(cpu_values)

    print(f"Reading amount: {len(cpu_values)}")
    print(f"Max CPU: {max_cpu:.1f}%")
    print(f"Min CPU: {min_cpu:.1f}%")
    print(f"Average CPU: {avg_cpu:.1f}%")