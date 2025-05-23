#
#
#  Basic for scraping data from static pages
#
# ------ IMPORTANT! ------
# if you need return soup object:
# you cand import from __utils -> GetHtmlSoup
# if you need return regex object:
# you cand import from __utils ->
# ---> get_data_with_regex(expression: str, object: str)
#
# Company ---> luxoft
# Link ------> https://career.luxoft.com/jobs?keyword=&country[]=Romania&perPage=120
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_county_json,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    """
    ... scrape data from luxoft scraper.
    """
    soup = GetStaticSoup(
        "https://career.luxoft.com/jobs?keyword=&country[]=Romania&perPage=120")

    job_list = []
    for job in soup.find_all("a", class_="jobs__list__job"):
        city = job.find("p", class_="body-s-regular").text.strip()
        if "Bucharest" in city:
            city = "Bucuresti"

        # get jobs items from response
        job_list.append(Item(
            job_title=job.find(
                "h2", class_="subtitle-l text-rich-black").text.strip(),
            job_link="https://career.luxoft.com"+job.get("href"),
            company="luxoft",
            country="România",
            county="all" if "Remote" in city else city,
            city="all" if "Remote" in city else city,
            remote=get_job_type(city),
        ).to_dict())

    return job_list


def main():
    """
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    """

    company_name = "luxoft"
    logo_link = "https://s.dou.ua/CACHE/images/img/static/companies/Luxoft_Purple_RGB/b0bd318ade945671cd9b7d6d1c79191a.png"

    jobs = scraper()
    print("jobs found:", len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
