import requests, datetime, os, json
from bs4 import BeautifulSoup
from src.parser import parse_pdf   # we’ll write this next

GEM_BASE = "https://gem.gov.in"
LIST_URL = f"{GEM_BASE}/tenders?tab=active&page=1"

def fetch_today_list():
    resp = requests.get(LIST_URL, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select("table.tender-list tr")[1:4]  # first 3 rows
    links = [GEM_BASE + r.find("a")["href"] for r in rows if r.find("a")]
    return links

def download_parse(link, out_dir):
    pdf_url = link.replace("/view/", "/download/") + ".pdf"
    pdf_path = os.path.join(out_dir, os.path.basename(pdf_url))
    os.makedirs(out_dir, exist_ok=True)
    with requests.get(pdf_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(pdf_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    # parse
    json_path = pdf_path.replace(".pdf", ".json")
    tender_json = parse_pdf(pdf_path)        # we’ll implement next
    with open(json_path, "w") as f:
        json.dump(tender_json, f, indent=2)
    return json_path

def scrape(date_str):
    out = f"data/tenders/{date_str}"
    links = fetch_today_list()
    json_files = []
    for l in links:
        try:
            json_files.append(download_parse(l, out))
        except Exception as e:
            print("skip", l, e)
    return json_files