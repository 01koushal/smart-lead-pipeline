from flask import Flask, render_template
from flask import request
import json

from services.scraper import scrape_website
from services.ai_service import generate_business_report

app = Flask(__name__)


def log_section(title, value=None):
    print(f"\n========== {title} ==========", flush=True)
    if value is not None:
        print(value, flush=True)

@app.route('/')
def home():
    # Renders index.html and passes a variable to it
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission
    name = request.form['fullName']
    email = request.form['workEmail']
    url=request.form['companyWebsite']

    log_section("FORM SUBMITTED", f"Name={name}\nEmail={email}\nURL={url}")

    scraped = scrape_website(url)

    log_section(
        "SCRAPED DATA RETURNED TO FLASK",
        json.dumps(scraped, indent=2, ensure_ascii=False)
    )

    log_section("GENERATING AI REPORT")
    report = generate_business_report(scraped)
    log_section("GENERATED AI REPORT", report)

    return render_template('index.html', message=f"Form submitted successfully! Hello, {name} ({email})!")

if __name__ == '__main__':
    # Runs the app locally on http://127.0.0.1:5000
    app.run(debug=True)
