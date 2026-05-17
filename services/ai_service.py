from groq import Groq
from dotenv import load_dotenv
import os
import json

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# -----------------------------------
# INITIALIZE GROQ CLIENT
# -----------------------------------

client = Groq(api_key=api_key)

# -----------------------------------
# GENERATE BUSINESS REPORT
# -----------------------------------

def generate_business_report(scraped_data):

    # -----------------------------------
    # BLOCKED WEBSITE HANDLING
    # -----------------------------------

    if scraped_data.get("blocked"):

        return """
BUSINESS AUDIT REPORT

COMPANY OVERVIEW:
The submitted website appears to use anti-bot or security verification systems,
which limited automated business analysis.

OBSERVATION:
The platform is protected by automated verification layers
that restrict direct content extraction from external systems.

RECOMMENDATIONS:
- Allow limited public-facing metadata for automated analysis tools
- Provide clearer business overview content
- Improve accessibility for external integrations and AI systems

OVERALL ASSESSMENT:
The system detected website protection mechanisms successfully
and avoided generating misleading insights from incomplete content.
"""

    # -----------------------------------
    # EXTRACT SCRAPED DATA
    # -----------------------------------

    title = scraped_data.get("title", "")
    meta_description = scraped_data.get(
        "meta_description", ""
    )

    headings = scraped_data.get("headings", [])

    business_summary = scraped_data.get(
        "business_summary", ""
    )

    # -----------------------------------
    # BUILD CONTEXT
    # -----------------------------------

    context = f"""
Website Title:
{title}

Meta Description:
{meta_description}

Headings:
{", ".join(headings)}

Business Summary:
{business_summary}
"""

    # -----------------------------------
    # AI PROMPT
    # -----------------------------------

    prompt = f"""
You are an expert AI business consultant.

Analyze the following company website information
and generate a professional business audit report.

Focus on:
- understanding the business
- identifying company positioning
- strengths
- growth opportunities
- business recommendations
- website improvement suggestions

Maintain a professional consulting tone.

COMPANY DATA:
{context}

Generate the report in the following format:

COMPANY OVERVIEW:
(2-3 sentences)

KEY STRENGTHS:
- point 1
- point 2
- point 3

GROWTH OPPORTUNITIES:
- point 1
- point 2
- point 3

RECOMMENDATIONS:
- point 1
- point 2
- point 3

OVERALL ASSESSMENT:
(short professional conclusion)
"""

    # -----------------------------------
    # GENERATE AI RESPONSE
    # -----------------------------------

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a professional AI business analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
            max_tokens=1200
        )

        report = response.choices[0].message.content

        return report

    # -----------------------------------
    # ERROR HANDLING
    # -----------------------------------

    except Exception as e:

        return f"""
AI REPORT GENERATION FAILED

ERROR:
{str(e)}
"""


# -----------------------------------
# TESTING
# -----------------------------------

if __name__ == "__main__":

    with open(
        "scraped_data.json",
        "r",
        encoding="utf-8"
    ) as file:

        scraped_data = json.load(file)

    report = generate_business_report(
        scraped_data
    )

    print("\n========== AI BUSINESS REPORT ==========\n")

    print(report)