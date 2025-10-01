import json

# Load IPs from cmoses_client.json
with open('cmoses_client.json', 'r') as f:
    ip_data = json.load(f)
    ip_list = [entry['ip'] for entry in ip_data if 'ip' in entry]  # Extract only IPs

# Load IPs from target_client.json
with open('target_client.json', 'r') as f:
    target_data = json.load(f)
    target_ips = [entry['ip'] for entry in target_data if 'ip' in entry]
    ip_list.extend(target_ips)  # Add target_client.json IPs to the list

# Remove duplicates from the IP list
ip_list = list(set(ip_list))  # Ensure ip_list contains only unique IPs

# Open http-2.log and process each line
results = {ip: {"count": 0, "entries": []} for ip in ip_list}  # Initialize results with count and entries
with open('http-2.log', 'r') as log_file:
    for line in log_file:
        try:
            log_entry = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip malformed lines
        for ip in ip_list:
            if log_entry.get('src_ip') == ip or log_entry.get('dest_ip') == ip:
                results[ip]["entries"].append(log_entry)  # Add the log entry
                results[ip]["count"] += 1  # Increment the count

# Output results as JSON
with open('matched_logs.json', 'w') as out_file:
    json.dump(results, out_file, indent=2)
