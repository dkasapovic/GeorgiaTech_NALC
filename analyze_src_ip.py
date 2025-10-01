import csv
import json

# Load inventory IP-to-employee mapping
inventory_file = "inventory-2.csv"
ip_to_employee = {}
with open(inventory_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ip_to_employee[row['IP']] = row['Employee']

# Analyze log file and collect results in two arrays
log_file = "http-2-srv-42-sanchez-brown.json"
get_calls = []
post_calls = []

with open(log_file, encoding='utf-8') as f:
    log_data = json.load(f)
    for entry in log_data.values():
        data = entry.get('data', {})
        src_ip = data.get('src_ip')
        http_method = data.get('http.http_method')
        employee = ip_to_employee.get(src_ip, "Unknown")
        result = {
            "http_method": http_method,
            "src_ip": src_ip,
            "employee": employee,
            "log_line": json.dumps(data)
        }
        if http_method == "GET":
            get_calls.append(result)
        elif http_method == "POST":
            post_calls.append(result)

# Write both arrays to a single JSON file
output_file = "employee_correlation.json"
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump({"get": get_calls, "post": post_calls}, out, indent=2)