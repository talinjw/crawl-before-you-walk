import requests
import bs4
from selenium import webdriver
import pandas as pd
from pprint import pprint
from datetime import datetime

def get_job_titles(soup):
    jobs = []
    inlines = soup.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    for inline in inlines:
            jobs.append(inline['title'])
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

def get_posting_ages(soup):
    posting_ages = []
    divs = soup.find_all(name='div', attrs={'class':'result-link-bar'})
    for div in divs:
        span = div.find(name='span', attrs={'class':'date'})
        if span == None:
            posting_ages.append("No age found")
        else:
            posting_ages.append(span.text)
    return(posting_ages)

def get_links(soup):
    links = []
    inlines = soup.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    for inline in inlines:
            links.append('www.indeed.com' + str(inline['href']))
    return(links)

def np_exists(soup):
    if soup.find(name='span', attrs={'class':'np'}) != None:
        page_exists = True
    else:
        page_exists = False
    return(page_exists)

def get_np_url(soup):
    div = soup.find(name='div', attrs={'class':'pagination'})
    inlines = div.find_all(name='a')
    np_url = 'https://www.indeed.com/' + str(list(inlines)[-1]['href'])
    return(np_url)

search_keyword = 'firefighter'
search_location = 'Bay Area, CA'

search_what = 'jobs?q=' + search_keyword
search_where = '&l=' + search_location

search_query = search_what + search_where
print(search_query)

url = 'https://www.indeed.com/' + search_query

# navigate to indeed via selenium passing url
browser = webdriver.Chrome()
browser.get(url)
html = browser.page_source
#html = requests.get(url)
soup = bs4.BeautifulSoup(html, 'html.parser')

all_jobs = []
all_companies = []
all_locations = []
all_summaries = []
all_posting_ages = []
all_links = []

nextpage_exists = np_exists(soup)
while nextpage_exists == True:
    all_jobs = get_job_titles(soup)
    all_companies = get_job_titles(soup)
    all_locations = get_locations(soup)
    all_summaries = get_summaries(soup)
    all_posting_ages = get_posting_ages(soup)
    all_links = get_links(soup)
    nextpage_url = get_np_url(soup)
    browser.get(nextpage_url)
    if browser.find_element_by_css_selector('#popover-x-button') != None:
        print(browser.find_element_by_css_selector('#popover-x-button'))
        browser.find_element_by_css_selector('#popover-x-button').click()
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    nextpage_exists = np_exists(soup)
else:
    all_jobs = all_jobs.append(get_job_titles(soup))
    all_companies = all_companies.append(get_job_titles(soup))
    all_locations = all_locations.append(get_locations(soup))
    all_summaries = all_summaries.append(get_summaries(soup))
    all_posting_ages = all_posting_ages.append(get_posting_ages(soup))
    all_links = all_links.append(get_links(soup))

print('Print current # of jobs: ' + str(len(all_jobs)))
print('Print current # of companies: ' + str(len(all_companies)))
print('Print current # of locations: ' + str(len(all_locations)))
print('Print current # of summaries: ' + str(len(all_summaries)))
print('Print current # of ages: ' + str(len(all_posting_ages)))
print('Print current # of links: ' + str(len(all_links)))    

#pprint(all_jobs)
#pprint(all_companies)
#pprint(all_locations)
#pprint(all_summaries)
#pprint(all_posting_ages)
#pprint(all_links)
    
date_time = datetime.now().time()
aggregate_all = pd.DataFrame(
    {'Job_Title': all_jobs,
     'Company_Name': all_companies,
     'Location': all_locations,
     'Job_Summary': all_summaries,
     'Posting_Age': all_posting_ages,
     'Link': all_links})

aggregate_all.to_csv(str(date_time) + '_' + search_keyword.upper() + '.csv')

