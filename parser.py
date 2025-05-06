import os
import fitz  # PyMuPDF
import re
import pandas as pd

# ---------- Custom Field Extraction Functions ----------

def extract_email(text):
    matches = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]+", text)
    return matches[0] if matches else ""

def extract_phone(text):
    normalized_text = text.replace('\n', ' ').replace('\r', ' ')

    phone_patterns = [
        r"(?:Phone|Mobile|Contact)[\s:]*([\+91\- ]*\d{5}[\s\-]*\d{5})",  # Group 1: after labels
        r"\b[\+91\- ]*\d{5}[\s\-]*\d{5}\b",  # No group
    ]

    for pattern in phone_patterns:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            raw_number = match.group(1) if match.lastindex else match.group(0)
            digits_only = re.sub(r"[^\d]", "", raw_number)
            if len(digits_only) >= 10:
                return int(digits_only[-10:])  # Keep last 10 digits to standardize Indian numbers
    return ""



def extract_name_from_filename(filename):
    base_name = os.path.splitext(filename)[0]
    match = re.match(r"Naukri_(.+?)\[\d+y_\d+m\]$", base_name)
    if match:
        raw_name = match.group(1)
        name_parts = raw_name.replace('_', ' ').split()
        return ' '.join(part.capitalize() for part in name_parts)
    return ""

# ---------- PDF Text Extraction ----------

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

# ---------- Resume Processing ----------

def process_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    filename = os.path.basename(pdf_path)
    return {
        "Name": extract_name_from_filename(filename),
        "Email": extract_email(text),
        "Phone": extract_phone(text)
    }

# ---------- Main ----------

def main():
    folder = "Resume"
    results = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if filename.endswith(".pdf"):
            print(f"Processing: {filename}")
            results.append(process_resume(filepath))
        else:
            print(f"Unsupported file type: {filename}")

    df = pd.DataFrame(results)
    try:
        df.to_csv("extracted_resume_data.csv", index=False)
        print("Data saved successfully to extracted_resume_data.csv.")
    except PermissionError:
        print("Permission denied. Please close 'extracted_resume_data.csv' if it's open and try again.")

if __name__ == "__main__":
    main()
