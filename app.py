from unittest import result

from flask import Flask, render_template
from flask import request

from services.scraper import scrape_website

app = Flask(__name__)

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
    print(f"Received form submission: Name={name}, Email={email}, URL={url}", flush=True)
    result = scrape_website(url)
    print(result)
    return render_template('index.html', message=f"Form submitted successfully! Hello, {name} ({email})!")

if __name__ == '__main__':
    # Runs the app locally on http://127.0.0.1:5000
    app.run(debug=True)
