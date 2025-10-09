import os, json, pandas as pd, datetime
from src.matcher import match_tender
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.scraper import scrape

print("Nightly matcher started")

# 1. scrape today's live tenders
today = datetime.date.today().isoformat()
tender_jsons = scrape(today)          # list of JSON paths
all_matches = []

# 2. match each tender
for j in tender_jsons:
    matches = match_tender(j, "data/my_catalogue.csv", top_k=5)
    if matches:
        all_matches.append({"tender_file": j, "matches": matches})

# 3. email digest
if all_matches:
    html = "<h3>GeM Tender Digest</h3><ul>"
    for item in all_matches:
        tender_name = os.path.basename(item["tender_file"]).replace(".json","")
        html += f"<li>Tender {tender_name}<ul>"
        for m in item["matches"]:
            html += f"<li>{m['sku']} – score {m['score']}</li>"
        html += "</ul></li>"
    html += "</ul>"

    message = Mail(
        from_email="lyrix.unboxed@gmail.com",
        to_emails="kapilmadan14@gmail.com",
        subject=f"GeM Tender Digest {today}",
        html_content=html)
    sg = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
    sg.send(message)
    print("Email sent")
else:
    print("No matches today")