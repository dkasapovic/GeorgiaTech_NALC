import json
import re
from collections import defaultdict

log_file = "mail-2.log"
output_file = "target_client.json"
cmoses_output = "cmoses_client.json"
cmoses_text = "to=<cmoses@northamericanlumbercoalition.com>"

with open(log_file, "r") as f:
    lines = f.readlines()

# Group lines by message ID
msgid_pattern = re.compile(r'(\b[A-F0-9]{10,}\b):')
msgid_lines = defaultdict(list)
for line in lines:
    match = msgid_pattern.search(line)
    if match:
        msgid = match.group(1)
        msgid_lines[msgid].append(line.strip())

results = []
for msgid, group in msgid_lines.items():
    obj = {"msgid": msgid}
    # Extract from, to, client, ip, timestamp
    for line in group:
        if "from=<" in line:
            obj["from"] = line
            from_email_match = re.search(r'from=<([^>]+)>', line)
            obj["from_email"] = from_email_match.group(1) if from_email_match else None
            timestamp_match = re.match(r'^(\w+ \d+ \d+:\d+:\d+)', line)
            obj["timestamp"] = timestamp_match.group(1) if timestamp_match else None
        if "to=<" in line:
            obj["to"] = line
        if "client=unknown[" in line:
            obj["client"] = line
            ip_match = re.search(r'\[(\d+\.\d+\.\d+\.\d+)\]', line)
            obj["ip"] = ip_match.group(1) if ip_match else None
        if "connect from unknown[" in line:
            obj["connected_from"] = line
    # Only add if all required fields are present
    if "from_email" in obj and "to" in obj and "client" in obj:
        results.append(obj)

# Filter for cmoses
cmoses_results = [obj for obj in results if cmoses_text in obj.get("to", "")]

with open(output_file, "w") as out:
    json.dump(results, out, indent=2)

with open(cmoses_output, "w") as out:
    json.dump(cmoses_results, out, indent=2)