import json
import re

# Load the JSON data to get from_emails
with open('cmoses_client.json', 'r') as f:
    data = json.load(f)

from_emails = set(entry['from_email'] for entry in data if 'from_email' in entry)

# Prepare regex pattern for all from_emails
email_pattern = re.compile(
    r'from=<(' + '|'.join(re.escape(email) for email in from_emails) + r')>',
    re.IGNORECASE
)

results = {}

# Search mail-2.log for lines with matching from_emails
with open('mail-2.log', 'r') as log_file:
    for line in log_file:
        match = email_pattern.search(line)
        if match:
            email = match.group(1)
            results.setdefault(email, []).append(line.strip())

# Write results to a JSON file
with open('emails_from_list_in_log.json', 'w') as out_file:
    json.dump(results, out_file, indent=2)
