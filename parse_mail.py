import json
import re

log_file = "mail-2.log"
target_text = "client=unknown[122.249.102.194]"
output_file = "target_client.json"
cmoses_text = "to=<cmoses@northamericanlumbercoalition.com>"
cmoses_output = "cmoses_client.json"

with open(log_file, "r") as f:
    lines = f.readlines()

results = []
for i, line in enumerate(lines):
    if target_text in line:
        start = max(0, i - 3)
        if i - start == 3:  # Ensure there are 4 lines
            client_line = lines[start + 3].strip()
            ip_match = re.search(r'\[(\d+\.\d+\.\d+\.\d+)\]', client_line)
            ip = ip_match.group(1) if ip_match else None
            from_line = lines[start].strip()
            from_email_match = re.search(r'from=<([^>]+)>', from_line)
            from_email = from_email_match.group(1) if from_email_match else None
            timestamp_match = re.match(r'^(\w+ \d+ \d+:\d+:\d+)', from_line)
            timestamp = timestamp_match.group(1) if timestamp_match else None
            obj = {
                "from": from_line,
                "from_email": from_email,
                "timestamp": timestamp,
                "to": lines[start + 1].strip(),
                "connected_from": lines[start + 2].strip(),
                "client": client_line,
                "ip": ip
            }
            results.append(obj)

cmoses_results = []
for i, line in enumerate(lines):
    if cmoses_text in line:
        start = i
        # Ensure indices are valid
        if start - 1 >= 0 and start + 2 < len(lines):
            from_line = lines[start - 1].strip()
            from_email_match = re.search(r'from=<([^>]+)>', from_line)
            from_email = from_email_match.group(1) if from_email_match else None
            timestamp_match = re.match(r'^(\w+ \d+ \d+:\d+:\d+)', from_line)
            timestamp = timestamp_match.group(1) if timestamp_match else None
            connected_from_line = lines[start + 1].strip()
            ip_match = re.search(r'\[(\d+\.\d+\.\d+\.\d+)\]', connected_from_line)
            ip = ip_match.group(1) if ip_match else None
            obj = {
                "from": from_line,
                "from_email": from_email,
                "timestamp": timestamp,
                "to": lines[start].strip(),
                "connected_from": connected_from_line,
                "client": lines[start + 2].strip(),
                "ip": ip
            }
            cmoses_results.append(obj)

with open(output_file, "w") as out:
    json.dump(results, out, indent=2)

with open(cmoses_output, "w") as out:
    json.dump(cmoses_results, out, indent=2)