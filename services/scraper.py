from playwright.sync_api import sync_playwright
import json

# -----------------------------------
# WEBSITE SCRAPER
# -----------------------------------

def scrape_website(url):

    # -----------------------------------
    # STRUCTURED BUSINESS DATA
    # -----------------------------------

    data = {
        "website": url,
        "title": "",
        "meta_description": "",
        "headings": [],
        "paragraphs": [],
        "cta_buttons": [],
        "business_summary": "",
        "blocked": False,
        "error": None
    }

    # -----------------------------------
    # HELPER FUNCTION
    # -----------------------------------

    def clean_text(text):
        return " ".join(text.split()).strip()

    # -----------------------------------
    # START SCRAPING
    # -----------------------------------

    try:

        with sync_playwright() as p:

            # Launch browser
            browser = p.chromium.launch(headless=True)

            # Create page
            page = browser.new_page()

            # Open website
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            # -----------------------------------
            # TITLE
            # -----------------------------------

            try:
                data["title"] = clean_text(page.title())
            except:
                pass

            # -----------------------------------
            # META DESCRIPTION
            # -----------------------------------

            try:

                meta_locator = page.locator(
                    'meta[name="description"]'
                )

                if meta_locator.count() > 0:

                    meta_description = meta_locator.first.get_attribute(
                        "content"
                    )

                    if meta_description:

                        data["meta_description"] = clean_text(
                            meta_description
                        )

            except:
                pass

            # -----------------------------------
            # HEADINGS
            # -----------------------------------

            try:

                headings = page.locator("h1, h2").all()

                for heading in headings:

                    text = clean_text(
                        heading.inner_text(timeout=3000)
                    )

                    if (
                        text
                        and len(text) > 3
                        and text not in data["headings"]
                    ):

                        data["headings"].append(text)

            except:
                pass

            # -----------------------------------
            # PARAGRAPHS
            # -----------------------------------

            try:

                paragraphs = page.locator("p").all()

                for p_tag in paragraphs:

                    text = clean_text(
                        p_tag.inner_text(timeout=3000)
                    )

                    # Filter noisy/short content
                    if (
                        text
                        and len(text) > 40
                        and text not in data["paragraphs"]
                    ):

                        data["paragraphs"].append(text)

            except:
                pass

            # -----------------------------------
            # CTA BUTTONS
            # -----------------------------------

            try:

                buttons = page.locator("button").all()

                for button in buttons:

                    text = clean_text(
                        button.inner_text(timeout=3000)
                    )

                    if (
                        text
                        and len(text) < 40
                        and text.lower() not in [
                            "home",
                            "about",
                            "contact",
                            "menu"
                        ]
                        and text not in data["cta_buttons"]
                    ):

                        data["cta_buttons"].append(text)

            except:
                pass

            # -----------------------------------
            # BUILD BUSINESS SUMMARY
            # -----------------------------------

            summary_parts = []

            if data["meta_description"]:

                summary_parts.append(
                    data["meta_description"]
                )

            if data["headings"]:

                summary_parts.extend(
                    data["headings"][:3]
                )

            if data["paragraphs"]:

                summary_parts.extend(
                    data["paragraphs"][:2]
                )

            data["business_summary"] = clean_text(
                " ".join(summary_parts)
            )

            # -----------------------------------
            # BLOCKED WEBSITE DETECTION
            # -----------------------------------

            blocked_keywords = [
                "just a moment",
                "security verification",
                "verify you are not a bot",
                "verification successful",
                "cloudflare",
                "access denied",
                "checking your browser"
            ]

            combined_text = (
                data["title"] + " " +
                data["business_summary"]
            ).lower()

            for keyword in blocked_keywords:

                if keyword in combined_text:

                    data["blocked"] = True

                    break

            # Close browser
            browser.close()

    # -----------------------------------
    # GLOBAL ERROR HANDLING
    # -----------------------------------

    except Exception as e:

        data["error"] = str(e)

        print("\nScraping failed:")
        print(e)

    # -----------------------------------
    # SAVE JSON
    # -----------------------------------

    with open(
        "scraped_data.json",
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            data,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    # -----------------------------------
    # PRINT RESULTS
    # -----------------------------------

    print("\nScraping completed successfully")

    print("\nTITLE:")
    print(data["title"])

    print("\nMETA DESCRIPTION:")
    print(data["meta_description"])

    print("\nHEADINGS:")
    for heading in data["headings"]:
        print("-", heading)

    print("\nCTA BUTTONS:")
    for button in data["cta_buttons"]:
        print("-", button)

    print("\nBUSINESS SUMMARY:")
    print(data["business_summary"])

    print("\nBLOCKED WEBSITE:")
    print(data["blocked"])

    if data["error"]:

        print("\nERROR:")
        print(data["error"])

    return data