import os, json, pandas as pd, datetime, smtplib, ssl
from email.mime.text import MIMEText
from src.matcher import match_tender

print("Nightly matcher started")

# fallback: use dummy tender so pipeline completes
tender_jsons = ["data/tender.json"]   # existing dummy file
all_matches = []

# 2. match each tender
for j in tender_jsons:
    matches = match_tender(j, "data/my_catalogue.csv", top_k=5)
    if matches:
        all_matches.append({"tender_file": j, "matches": matches})

# 3. email digest via Gmail SMTP
if all_matches:
    html = "<h3>GeM Tender Digest</h3><ul>"
    for item in all_matches:
        tender_name = os.path.basename(item["tender_file"]).replace(".json","")
        html += f"<li>Tender {tender_name}<ul>"
        for m in item["matches"]:
            html += f"<li>{m['sku']} – score {m['score']}</li>"
        html += "</ul></li>"
    html += "</ul>"

    msg = MIMEText(html, "html")
    msg["Subject"] = f"GeM Tender Digest {datetime.date.today().isoformat()}"
    msg["From"] = "lyrix.unboxed@gmail.com"
    msg["To"] = "kapilmadan14@gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("lyrix.unboxed@gmail.com", os.getenv("GMAIL_APP_PW"))
        server.send_message(msg)
    print("Gmail sent")
else:
    print("No matches today")