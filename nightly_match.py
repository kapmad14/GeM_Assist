import os, json, pandas as pd
from src.matcher import match_tender
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

print("Nightly matcher started")
tender = json.loads('{"buyer_name":"ABC","delivery_state":"MH","bid_deadline":"2025-10-20","products":[{"description":"Stainless steel bench","quantity":5,"uom":"NOS"}]}')
with open("data/tender.json","w") as f:
    json.dump(tender,f)

matches = match_tender("data/tender.json", "data/my_catalogue.csv", top_k=5)
print(json.dumps(matches, indent=2))
print("Done")

if matches:
    html = "<h3>Top matches</h3><ul>"
    for m in matches:
        html += f"<li>{m['sku']} – score {m['score']}</li>"
    html += "</ul>"

    message = Mail(
        from_email="gem@yourdomain.com",
        to_emails="YOUR_EMAIL@example.com",
        subject="GeM Tender Digest",
        html_content=html)
    sg = SendGridAPIClient(os.getenv("SENDGRID_KEY"))
    sg.send(message)
    print("Email sent")