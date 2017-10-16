import requests
import bs4 
import pandas as pd
from list_jobs import get_all_parameters_for_all_listings

# Build search_query and get dataframe containing all associated links
search_keyword = 'firefighter'
search_location = 'Bay Area, CA'
search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
search_url = 'https://www.indeed.com/' + search_query
print(search_url)

df_all_parameters = get_all_parameters_for_all_listings(search_url)

# Store all links associated with search_query in a list; loop through that list
all_links = df_all_parameters['Link'].tolist()
 
for link in all_links:
    current_url = 'https://' + link

    response = requests.get(current_url)
    print(response.status_code)
    
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # Get all the text from a given page
    page_text = soup.findAll(text=True)
    print(page_text)
    
