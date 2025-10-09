import json, openai, os, PyPDF2

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_pdf(pdf_path):
    # placeholder: returns dummy JSON
    reader = PyPDF2.PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    prompt = 'Return JSON only: {"buyer_name":"...","delivery_state":"...","bid_deadline":"YYYY-MM-DD","products":[{"description":"...","quantity":0,"uom":"..."}]}'
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt + "\n\n" + text[:12000]}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)