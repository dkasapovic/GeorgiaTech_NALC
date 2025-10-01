import json, pathlib

src = pathlib.Path("http-2.log")
out = pathlib.Path("http-2-srv-42-sanchez-brown.json")

matches = []
with src.open("r", encoding="utf-8", errors="replace") as f:
    for line_no, line in enumerate(f, 1):
        t = line.strip()
        # Skip empty and plain hostname unless you want them
        if not t or t == "srv-42.sanchez-brown.com":
            continue
        try:
            obj = json.loads(t)
        except json.JSONDecodeError:
            continue
        if obj.get("http.hostname") == "srv-42.sanchez-brown.com":
            matches.append({"line_no": line_no, "data": obj})

# Write matches as a numbered dictionary
output_obj = {str(i+1): match for i, match in enumerate(matches)}

with out.open("w", encoding="utf-8") as w:
    json.dump(output_obj, w, indent=2)

print("Total matches:", len(matches))
print("First 3 line numbers:", [m["line_no"] for m in matches[:3]])
print("Last 3 line numbers:", [m["line_no"] for m in matches[-3:]])