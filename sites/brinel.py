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
# Company ---> BRINEL
# Link ------> https://www.brinel.ro/cariere#job-30
#
#
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    get_county_json,
    Item,
    UpdateAPI,
)


'''
    
    UpdateAPI().update_jobs(company_name: str, data_jobs: list)
    UpdateAPI().update_logo(id_company: str, logo_link: str)

    ########################################################################
'''


def scraper():
    '''
    ... scrape data from BRINEL scraper.
    '''
    soup = GetStaticSoup("https://www.brinel.ro/cariere#job-30")

    job_list = []
    for job in soup.find_all('div', attrs=('row align-items-center')):
        
        # Extrarct locaion from jobs
        city=job.find('span', attrs=('job--loc-type')).text.strip() if job.find('span', attrs=('job--loc-type')) != None else 'Cluj-Napoca'
        county=None if city == None else get_county_json(city)
        
         # Find span element with class 'btn' and get 'data-bs-target' attribute
        span = job.find('span', class_='btn')
        if span:
            link = span.get('data-bs-target')

        # get jobs items from response
        job_list.append(Item(
            job_title = job.find('h4').text.strip(),
            job_link='https://www.brinel.ro/cariere'+link,
            company='BRINEL',
            country='România',
            county=county,
            city=city,
            remote = get_job_type(''),
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "BRINEL"
    logo_link = "https://apcom.ro/assets/images/logo-brinel-1400x700.png"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
