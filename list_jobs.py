import requests
import bs4
import pandas as pd
from datetime import datetime
from pprint import pprint

def get_jobs(soup):
    jobs = []
    inline_elements = soup.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    for element in inline_elements:
            jobs.append(element['title'])
    return(jobs)

def get_companies(soup): 
    companies = []
    spans = soup.find_all(name='span', attrs={'class':'company'})
    for span in spans:
        companies.append(span.text)
    return(companies)

def get_locations(soup):
    locations = []
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)
    return(locations)

def get_summaries(soup):
    summaries = []
    spans = soup.findAll('span', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text)
    return(summaries)

def get_ages(soup):
    ages = []
    divs = soup.find_all(name='div', attrs={'class':'result-link-bar'})
    for div in divs:
        span = div.find(name='span', attrs={'class':'date'})
        if span == None:
            ages.append("No age found")
        else:
            ages.append(span.text)
    return(ages)

def get_links(soup):
    links = []
    inline_elements = soup.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    for element in inline_elements:
            links.append('www.indeed.com' + str(element['href']))
    return(links)

def does_a_nextpage_exist(soup):
    spans = soup.find_all(name='span', attrs={'class':'np'})
    for span in spans:
        if 'Next' in span.text:
            nextpage_exists = True
        else:
            nextpage_exists = False
    return(nextpage_exists)

def get_nextpage_url(soup):
    div = soup.find(name='div', attrs={'class':'pagination'})
    inline_elements = div.find_all(name='a')
    nextpage_url = 'https://www.indeed.com/' + str(list(inline_elements)[-1]['href'])
    return(nextpage_url)

search_keyword = 'firefighter'
search_location = 'Bay Area, CA'

field_what = 'jobs?q=' + search_keyword
field_where = '&l=' + search_location

search_query = field_what + field_where
print(search_query)

url = 'https://www.indeed.com/' + search_query
print(url)

response = requests.get(url)
print(response.status_code)

html = response.text

soup = bs4.BeautifulSoup(html, 'html.parser')

all_jobs = []
all_companies = []
all_locations = []
all_summaries = []
all_ages = []
all_links = []
page_counter = 1

while True:
    currentpage_jobs = get_jobs(soup)
    all_jobs.extend(currentpage_jobs)
    #pprint(all_jobs)

    currentpage_companies = get_companies(soup)
    all_companies.extend(currentpage_companies)
    #pprint(all_companies)

    currentpage_locations = get_locations(soup)
    all_locations.extend(currentpage_locations)
    #pprint(all_locations)
    
    currentpage_summaries = get_summaries(soup)
    all_summaries.extend(currentpage_summaries)
    #pprint(all_summaries)
    
    currentpage_ages = get_ages(soup)
    all_ages.extend(currentpage_ages)
    #pprint(all_ages)
    
    currentpage_links = get_links(soup)
    all_links.extend(currentpage_links)
    #pprint(all_links)

    # Check to see if this is the last page; if not, then navigate to the next page
    nextpage_exists = does_a_nextpage_exist(soup)
    print(nextpage_exists)
    if nextpage_exists == True:
        page_counter += 1
        print(page_counter)
        
        nextpage_url = get_nextpage_url(soup)
        print(nextpage_url)
        
        response = requests.get(nextpage_url)
        print(response.status_code)
        
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
    else:
        break

print('Print current # of jobs: ' + str(len(all_jobs)))
print('Print current # of companies: ' + str(len(all_companies)))
print('Print current # of locations: ' + str(len(all_locations)))
print('Print current # of summaries: ' + str(len(all_summaries)))
print('Print current # of ages: ' + str(len(all_ages)))
print('Print current # of links: ' + str(len(all_links)))    
    
date_time = datetime.now().time()
all_params = pd.DataFrame(
    {'Job_Title': all_jobs,
     'Company_Name': all_companies,
     'Location': all_locations,
     'Job_Summary': all_summaries,
     'Posting_Age': all_ages,
     'Link': all_links})

current_datetime = datetime.now()
print(current_datetime)

all_params.to_csv(current_datetime.strftime('%Y-%m-%d') + '_' + current_datetime.strftime('%H:%M:%S') + '_' + search_keyword.upper() + '.csv')
