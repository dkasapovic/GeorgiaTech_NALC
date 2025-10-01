import json

# Prompt the user to enter a specific IP address
search_ip = "10.10.2.207"

# Open http-2.log and process each line
results = {"count": 0, "entries": []}  # Initialize results with count and entries
with open('http-2.log', 'r') as log_file:
    for line in log_file:
        try:
            log_entry = json.loads(line)
        except json.JSONDecodeError:
            continue  # Skip malformed lines
        if log_entry.get('src_ip') == search_ip or log_entry.get('dest_ip') == search_ip:
            results["entries"].append(log_entry)  # Add the log entry
            results["count"] += 1  # Increment the count

# Output results as JSON
output_file = f'matched_logs_{search_ip}.json'
with open(output_file, 'w') as out_file:
    json.dump(results, out_file, indent=2)
