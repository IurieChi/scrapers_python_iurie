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
# Company ---> ENGIE
# Link ------> https://jobs.engie.com/search/?q=&locationsearch=Romania
#
#
import time
from __utils import (
    GetStaticSoup,
    get_county,
    get_job_type,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from ENGIE scraper.
    '''
    page = 0
    flag = True
    job_list = []
    
    while flag:
        soup = GetStaticSoup(f"https://jobs.engie.com/search/?q=&locationsearch=Romania&startrow={page}")
        # print(soup)
        if len(jobs := soup.find_all('tr', attrs=('data-row'))) >0:
            for job in jobs:
                # link = 'https://jobs.engie.com'+ job.find('a')['href']
                # for item in link:
                #     s = GetStaticSoup(item)
                #     print(s.find('div',class__ = 'job').text)
                # Remove "Romania" from the location --- Start
                city_location = job.find('span', attrs ='jobLocation').text.strip().title().split(', R')[0].split(', ')
                
                # Check if 'COURBEVOIE' exists in the list
                if 'COURBEVOIE'.title() in city_location:
                    # Replace all elements with just 'all'
                    city_location = ['all']
                    
                for city in range(len(city_location)):
                    if 'Bucharest' in city_location[city]:
                        city_location[city]='București'  
                    if 'Pi' in city_location[city]:
                        city_location[city]='Pitesti'
                    if 'Crai' in city_location[city]:
                        city_location[city]='Craiova'
                    if 'Ploiest' in city_location[city]:
                        city_location[city] = 'Ploiesti'
                    if 'Turnu Mag' in  city_location[city]:
                        city_location[city] = 'Turnu Magurele'
                  
                # check county for cities from city_loc list  add to a county list if True else not then None 
                job_county = [get_county(city)[0] if True in get_county(city) else None for city in city_location]
                
                # get jobs items from response
                job_list.append(Item(
                    job_title = job.find('a', attrs='jobTitle-link').text,
                    job_link='https://jobs.engie.com'+ job.find('a')['href'],
                    company='ENGIE',
                    country='România',
                    county = job_county,
                    city = 'all'  if not None in job_county and  job_county[0]!='Bucuresti' else  city_location,
                    # for location if all then location remote else On-site
                    remote =  get_job_type('remote') if "all" in city_location else get_job_type(''),
                ).to_dict())
    
        else:
            flag = False
        
        # increment page
        page += 25
        time.sleep(1)
    
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "ENGIE"
    logo_link = "https://rmkcdn.successfactors.com/c4851ec3/1960b45a-f47f-41a6-b1c7-c.svg"

    jobs = scraper()
    print(len(jobs))
    # uncomment if your scraper done
    UpdateAPI().publish(jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
