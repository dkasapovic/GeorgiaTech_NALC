import json
import re
from collections import defaultdict

# Load JSON data
with open('cmoses_client.json', 'r') as f:
    data = json.load(f)

# Build a mapping of ip -> list of message IDs
ip_to_msgids = defaultdict(list)
for entry in data:
    ip = entry.get('ip')
    if ip:
        match = re.search(r'postfix/qmgr\[\d+\]: ([A-F0-9]+):', entry.get('from', ''))
        if match:
            ip_to_msgids[ip].append(match.group(1))

# Read mail-2.log once and index by message ID
results = defaultdict(list)
with open('mail-2.log', 'r') as log_file:
    for line in log_file:
        if 'from=' in line:
            for ip, msgids in ip_to_msgids.items():
                for msgid in msgids:
                    if msgid in line:
                        results[ip].append(line.strip())

# Save results as JSON
with open('ip_search_results.json', 'w') as out_file:
    json.dump(results, out_file, indent=2)