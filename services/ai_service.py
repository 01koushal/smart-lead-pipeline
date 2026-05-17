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
# DEFAULT REPORT STRUCTURE
# -----------------------------------

def empty_report(message="Unable to generate report."):

    return {
        "business_score": 0,
        "market_position": 0,
        "ai_innovation": 0,
        "growth_potential": 0,

        "executive_summary": message,

        "business_positioning": [],
        "key_strengths": [],
        "growth_opportunities": [],
        "website_analysis": [],

        "strategic_recommendations": [],

        "overall_assessment":
        "Unable to generate assessment."
    }

# -----------------------------------
# GENERATE BUSINESS REPORT
# -----------------------------------

def generate_business_report(scraped_data):

    # -----------------------------------
    # BLOCKED WEBSITE HANDLING
    # -----------------------------------

    if scraped_data.get("blocked"):

        return {
            "business_score": 45,
            "market_position": 40,
            "ai_innovation": 35,
            "growth_potential": 50,

            "executive_summary":
            "The submitted website appears to use anti-bot or security verification systems which limited automated business analysis.",

            "business_positioning": [
                "Website protected using verification systems",
                "Public business visibility is partially restricted"
            ],

            "key_strengths": [
                "Strong security infrastructure",
                "Protection against automated abuse"
            ],

            "growth_opportunities": [
                "Allow limited metadata visibility",
                "Improve public business accessibility"
            ],

            "website_analysis": [
                "Bot protection detected",
                "Automated content extraction restricted"
            ],

            "strategic_recommendations": [
                {
                    "title": "Improve AI Accessibility",
                    "priority": 82
                },
                {
                    "title": "Enhance Public Metadata",
                    "priority": 75
                }
            ],

            "overall_assessment":
            "The system detected website protection mechanisms successfully and avoided generating misleading insights from incomplete content."
        }

    # -----------------------------------
    # EXTRACT SCRAPED DATA
    # -----------------------------------

    title = scraped_data.get("title", "")

    meta_description = scraped_data.get(
        "meta_description",
        ""
    )

    headings = scraped_data.get(
        "headings",
        []
    )

    business_summary = scraped_data.get(
        "business_summary",
        ""
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
You are a senior AI business consultant.

Analyze the company data and generate a STRICT VALID JSON response.

IMPORTANT RULES:
- Return ONLY VALID JSON
- No markdown
- No explanations
- No ```json
- Scores must be between 1 and 100
- Keep content professional
- Arrays must contain short meaningful points

JSON FORMAT:

{{
  "business_score": 85,
  "market_position": 78,
  "ai_innovation": 91,
  "growth_potential": 74,

  "executive_summary": "short professional summary",

  "business_positioning": [
    "point 1",
    "point 2"
  ],

  "key_strengths": [
    "point 1",
    "point 2",
    "point 3"
  ],

  "growth_opportunities": [
    "point 1",
    "point 2"
  ],

  "website_analysis": [
    "point 1",
    "point 2"
  ],

  "strategic_recommendations": [
    {{
      "title": "recommendation title",
      "priority": 88
    }},
    {{
      "title": "recommendation title",
      "priority": 76
    }}
  ],

  "overall_assessment": "final assessment paragraph"
}}

COMPANY DATA:
{context}
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

        print("\n========== RAW AI RESPONSE ==========\n")
        print(report)

        # -----------------------------------
        # CLEAN RESPONSE
        # -----------------------------------

        cleaned = report.strip()

        # remove markdown if model adds it
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

        # -----------------------------------
        # CONVERT JSON STRING -> PYTHON DICT
        # -----------------------------------

        parsed_report = json.loads(cleaned)

        return parsed_report

    # -----------------------------------
    # JSON ERROR
    # -----------------------------------

    except json.JSONDecodeError as e:

        print("\nJSON PARSE ERROR:")
        print(e)

        return empty_report(
            f"Failed to parse AI JSON response: {str(e)}"
        )

    # -----------------------------------
    # GENERAL ERROR
    # -----------------------------------

    except Exception as e:

        print("\nAI GENERATION ERROR:")
        print(e)

        return empty_report(
            f"AI REPORT GENERATION FAILED: {str(e)}"
        )

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

    print("\n========== FINAL PARSED REPORT ==========\n")

    print(json.dumps(report, indent=4))