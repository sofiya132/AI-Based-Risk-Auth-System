# Run this Python script once to generate the CSV
# Save as: backend/ml/generate_csv.py

import csv
import random

rows = []
header = ["ip_match","device_match","hour_deviation","failed_attempts","geo_risk","browser_change","label"]
rows.append(header)

random.seed(42)

for _ in range(800):
    # Generate SAFE logins (label = 0)
    ip_match = 1
    device_match = 1
    hour_deviation = random.randint(0, 2)
    failed_attempts = random.randint(0, 1)
    geo_risk = 0
    browser_change = 0
    label = 0
    rows.append([ip_match, device_match, hour_deviation, failed_attempts, geo_risk, browser_change, label])

for _ in range(400):
    # Generate RISKY logins (label = 1)
    ip_match = random.choice([0, 0, 1])      # Mostly different IP
    device_match = random.choice([0, 0, 1])  # Mostly different device
    hour_deviation = random.randint(5, 12)   # Unusual hour
    failed_attempts = random.randint(2, 5)   # Multiple failures
    geo_risk = random.choice([0, 1, 1])      # Often different country
    browser_change = random.choice([0, 1])
    label = 1
    rows.append([ip_match, device_match, hour_deviation, failed_attempts, geo_risk, browser_change, label])

# Shuffle rows so safe/risky aren't all in order
random.shuffle(rows[1:])  # Don't shuffle the header

with open("login_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("login_data.csv created with", len(rows)-1, "rows")