from playwright.sync_api import sync_playwright
import pandas as pd


def scrape_remoteok(pages=5):

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_number in range(1, pages + 1):

            if page_number == 1:
                url = "https://remoteok.com/remote-data-jobs"
            else:
                url = f"https://remoteok.com/remote-data-jobs/{page_number}"

            print(f"Scraping {url}")

            page.goto(url)

            page.wait_for_timeout(3000)

            job_cards = page.query_selector_all("tr.job")

            for job in job_cards:

                title_el = job.query_selector("h2")
                company_el = job.query_selector("h3")

                title = title_el.inner_text() if title_el else None
                company = company_el.inner_text() if company_el else None

                if title and company:

                    jobs.append({
                        "job_title": title,
                        "company_name": company,
                        "company_location": "Remote",
                        "source": "remoteok"
                    })

        browser.close()

    df = pd.DataFrame(jobs)

    print("\nTotal jobs scraped:", len(df))
    print(df.head())

    return df


if __name__ == "__main__":
    scrape_remoteok()