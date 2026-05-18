# ProspectIQ – AI-Powered Personalized Business Audit Platform

## Overview

ProspectIQ is an AI-powered lead intelligence and automated business audit platform built as part of the SimplifIQ Software Developer Intern Assessment.

The system automates the entire workflow that businesses typically perform manually after receiving a lead submission:

* Capturing prospect details
* Researching the company
* Enriching business information
* Generating personalized insights
* Creating a professional PDF report
* Sending the report automatically via email
* Logging leads into Google Sheets

The goal of the project is to deliver a highly personalized and professional first interaction immediately after a prospect submits their company details.

---

# Live Demo

Frontend:

[https://prospectiq.koushal.in/](https://prospectiq.koushal.in/)

GitHub Repository:

[https://github.com/01koushal/smart-lead-pipeline](https://github.com/01koushal/smart-lead-pipeline)

---

# Features

## Lead Intake Workflow

* Collects:

  * Full Name
  * Work Email
  * Company Website

* Validates and processes submissions automatically.

---

## Website Intelligence & Enrichment

The system scrapes publicly available business information from the submitted website using Playwright.

Extracted data includes:

* Website title
* Meta description
* Headings
* Paragraph content
* CTA buttons
* Business summary

The scraper also detects:

* Cloudflare protection
* Anti-bot systems
* Restricted/blocked websites

---

## AI Business Analysis

The extracted company information is analyzed using Groq-hosted Llama models.

The AI system generates:

* Business score
* Market positioning score
* AI innovation score
* Growth potential score
* Executive summary
* Business positioning insights
* Key strengths
* Growth opportunities
* Website analysis
* Strategic recommendations
* Overall assessment

The AI output is enforced in strict JSON format for structured rendering and reliability.

---

## Professional PDF Report Generation

The platform generates a professional PDF report automatically.

Features:

* Dynamic company-specific insights
* Clean modern report styling
* Dynamic scoring system
* Recommendation scorecards
* Source data transparency section
* Structured sections and formatting

The report is generated using:

* Flask templating
* HTML/CSS
* xhtml2pdf

---

## Automated Email Delivery

After report generation:

* The generated PDF is archived
* A webhook is triggered automatically
* The report is downloaded dynamically
* The PDF is attached to an email
* The report is emailed automatically to the prospect

This workflow is powered using:

* n8n automation
* Gmail OAuth integration
* Webhook-based orchestration

---

## n8n Workflow Automation

The platform uses a deployed n8n workflow for orchestration and automation.

Workflow steps:

1. Flask backend sends a POST request to an n8n webhook
2. The webhook receives:

   * Name
   * Email
   * Company
   * Generated PDF URL
3. n8n downloads the generated PDF using an HTTP Request node
4. The PDF is attached automatically using the Gmail node
5. The report is emailed to the prospect
6. Lead data is appended into Google Sheets

The workflow includes:

* Webhook Trigger Node
* HTTP Request Node
* Gmail Node
* Google Sheets Node

This architecture separates automation workflows from the main Flask application and keeps the backend lightweight and maintainable.

---

## Webhook Integration

The Flask backend triggers the automation pipeline using an HTTP POST webhook request.

Payload sent to n8n includes:

```json
{
  "name": "Prospect Name",
  "email": "prospect@email.com",
  "company": "Company Name",
  "pdf_url": "Public PDF URL"
}
```

This webhook-driven design makes the automation pipeline modular and scalable.

---

## Google Sheets Logging (Bonus Feature)

Every lead submission is logged into Google Sheets.

Tracked fields include:

* Name
* Email
* Company
* Timestamp
* Report status

This acts as a lightweight CRM-style lead tracker.

---

# n8n Workflow Architecture

```text
Flask Backend
      ↓
POST Webhook Request
      ↓
n8n Webhook Trigger
      ↓
Download Generated PDF
      ↓
Send Email via Gmail Node
      ↓
Append Lead Data to Google Sheets
```

The n8n workflow handles asynchronous automation tasks separately from the core Flask application.

---

# System Architecture

```text
User Form Submission
        ↓
Flask Backend
        ↓
Website Scraper (Playwright)
        ↓
Structured Business Data
        ↓
Groq AI Analysis
        ↓
Structured JSON Report
        ↓
Dynamic PDF Generation
        ↓
n8n Webhook Automation
        ↓
Email Delivery + Google Sheets Logging
```

---

# Tech Stack

## Backend

* Python
* Flask

## AI Layer

* Groq API
* Llama Models

## Scraping

* Playwright

## PDF Generation

* xhtml2pdf
* HTML/CSS
* Jinja Templates

## Automation

* n8n
* Gmail API (via n8n Gmail node)
* Google Sheets API (via n8n Google Sheets node)

## Deployment

* Render

---

# Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── scraped_data.json
│
├── services/
│   ├── scraper.py
│   ├── ai_service.py
│   └── pdf_service.py
│
├── templates/
│   ├── index.html
│   └── report_template.html
│
├── static/
│
├── reports/
│
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/01koushal/smart-lead-pipeline.git
```

```bash
cd smart-lead-pipeline
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Playwright Browsers

```bash
playwright install
```

---

## 5. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Add any additional email or automation credentials if required.

---

## 6. Run Application

```bash
python app.py
```

Application runs at:

```text
http://127.0.0.1:5000
```
n8n Docker Deployment
The n8n automation service was deployed separately using Docker-based deployment on Render.

Docker Image
n8nio/n8n

Environment Configuration

The following environment variables were configured for deployment:
N8N_BASIC_AUTH_ACTIVE=true
N8N_HOST=<deployment-host>
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=<public-webhook-url>
---



# Engineering Decisions

## Why Playwright?

Many modern websites rely heavily on JavaScript rendering.

Playwright was chosen instead of simple requests-based scraping because it:

* Handles JS-rendered pages
* Works better with dynamic websites
* More closely simulates real browser behavior
* Provides better real-world scraping reliability

---

## Why Structured JSON AI Output?

Initially, the AI returned raw text reports.

The architecture was later improved to:

* Enforce strict JSON outputs
* Enable dynamic rendering
* Prevent hardcoded content
* Improve PDF consistency
* Reduce formatting failures

This makes the report system significantly more scalable and maintainable.

---

## Why xhtml2pdf?

Modern browser-based PDF rendering solutions were considered.

However, xhtml2pdf was selected because:

* Lightweight deployment
* Simpler Render compatibility
* Fewer native dependencies
* Faster setup for free-tier deployment

Tradeoff:

* Limited CSS support compared to Chromium-based renderers.

---

## Why Add Source Data Transparency?

AI-generated insights can occasionally contain estimation-based analysis.

To improve transparency and auditability:

* The final report includes extracted source information
* Users can verify how the AI derived its recommendations

This improves trust and reduces hallucination concerns.

---

# Real-World Handling & Fallbacks

The system includes handling for:

* Blocked websites
* Cloudflare protection
* Empty metadata
* Partial scraping failures
* AI JSON parsing failures
* Incomplete website content
* PDF generation edge cases

Fallback reports are generated instead of crashing the workflow.

---

# Known Limitations

* Some websites aggressively block automated scraping
* AI insights depend on publicly available website content
* xhtml2pdf has limited support for modern CSS features
* Render free tier may introduce cold-start delays
* The quality of analysis depends on website content richness

---

# Future Improvements

Potential future enhancements:

* Browser-based PDF rendering using Playwright/Puppeteer
* Better SEO analysis
* Social media enrichment
* Competitor benchmarking
* AI confidence scoring
* CRM integration
* Persistent database storage
* Multi-page analytics dashboards
* Company logo extraction
* Industry-specific audit templates

---

# Screenshots

Recommended screenshots to include:

* Homepage UI
* Form submission workflow
* Generated PDF report
* Email delivery
* Google Sheets logging
* Architecture diagram

---

# Security & Privacy Notes

* Only publicly available website information is analyzed
* No sensitive user credentials are stored
* Reports are generated dynamically per request
* AI analysis is based solely on extracted business-facing data

---

# Reflection

This project focused heavily on:

* End-to-end automation
* Real-world workflow reliability
* AI-assisted business analysis
* Practical deployment considerations
* Maintainable service separation
* Transparency in AI-generated insights

The primary goal was not just generating AI content, but building a production-style automated workflow that creates a professional first interaction for potential business leads.

---

# Author

Koushal Pala

GitHub:
[https://github.com/01koushal](https://github.com/01koushal)

LinkedIn:
[https://www.linkedin.com/](https://www.linkedin.com/)

---

# License

This project was created for educational and assessment purposes.
