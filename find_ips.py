import json
import glob

# Step 1: Collect dest_ip from all matched_logs_*.json files
json_files = glob.glob("matched_logs_*.json")
all_dest_ips = set()

for filename in json_files:
    with open(filename, "r") as f:
        data = json.load(f)
        for entry in data.get("entries", []):
            ip = entry.get("dest_ip")
            # Exclude dest_ip 122.249.102.194
            if ip and ip != "122.249.102.194":
                all_dest_ips.add(ip)

# Step 2: Search those IPs in http-2.log (src_ip or dest_ip)
matches = []
with open("http-2.log", "r") as logf:
    for line in logf:
        try:
            log_entry = json.loads(line)
            src_ip = log_entry.get("src_ip")
            dest_ip = log_entry.get("dest_ip")
            for ip in all_dest_ips:
                if ip == src_ip or ip == dest_ip:
                    matches.append(log_entry)
                    break
        except Exception:
            continue

# Step 3: Save results to a JSON file
with open("matched_http2_entries.json", "w") as outf:
    json.dump(matches, outf, indent=2)