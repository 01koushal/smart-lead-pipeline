from flask import Flask, render_template
from flask import request
import json
from flask import send_from_directory
import requests
from services.scraper import scrape_website
from services.ai_service import generate_business_report
from services.pdf_service import generate_pdf_report

app = Flask(__name__)

def log_section(title, value=None):

    print(f"\n========== {title} ==========", flush=True)

    if value is not None:
        print(value, flush=True)

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/reports/<path:filename>')
def download_report(filename):

    return send_from_directory(
        'reports',
        filename
    )

@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['fullName']
    email = request.form['workEmail']
    url = request.form['companyWebsite']

    log_section(
        "FORM SUBMITTED",
        f"Name={name}\nEmail={email}\nURL={url}"
    )

    scraped = scrape_website(url)

    log_section(
        "SCRAPED DATA RETURNED TO FLASK",
        json.dumps(scraped, indent=2, ensure_ascii=False)
    )

    log_section("GENERATING AI REPORT")

    report = generate_business_report(scraped)

    log_section("GENERATED AI REPORT", report)

    pdf_path = generate_pdf_report(
        company_name=name,
        report_data=report
    )
    try:

        public_pdf_url = (
            f"https://smart-lead-pipeline.onrender.com/{pdf_path}"
        )

        requests.post(
            "https://n8n-latest-eb59.onrender.com/webhook-test/0e761678-5bad-4ad4-b522-0e78ffd8ae4e",

            json={

                "name": name,
                "email": email,
                "company": request.form['companyName'],
                "pdf_url": public_pdf_url
            },

            timeout=15
        )

        print("\nN8N WEBHOOK SENT")

    except Exception as e:

        print("\nN8N WEBHOOK FAILED")
        print(e)
    

    return render_template(
        'index.html',
        message=f"Form submitted successfully! Hello, {name} ({email})!",
        pdf_path=pdf_path
    )

if __name__ == '__main__':

    app.run(debug=True)