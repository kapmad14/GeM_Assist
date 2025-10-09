import os, json, pandas as pd
from src.matcher import match_tender

print("Nightly matcher started")
tender = json.loads('{"buyer_name":"ABC","delivery_state":"MH","bid_deadline":"2025-10-20","products":[{"description":"Stainless steel bench","quantity":5,"uom":"NOS"}]}')
with open("data/tender.json","w") as f:
    json.dump(tender,f)

matches = match_tender("data/tender.json", "data/my_catalogue.csv", top_k=5)
print(json.dumps(matches, indent=2))
print("Done")