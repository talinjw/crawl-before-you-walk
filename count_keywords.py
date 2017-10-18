import requests
import bs4
import pandas as pd
from list_jobs import get_all_parameters_for_all_listings


def get_text(links):
    text_by_page = []

    for link in links:
        if 'http' in link:
            url = link
        else:
            url = 'https://' + link
        print(url)

        response = requests.get(url)
        print(response.status_code)

        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')

        page_text = soup.findAll(text=True)
        text_by_page.append(page_text)

    return(text_by_page)


# Build search_query and get a dataframe containing all associated links
search_keyword = 'firefighter'
search_location = 'Bay Area, CA'
search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
search_url = 'https://www.indeed.com/' + search_query
print(search_url)

df_all_parameters = get_all_parameters_for_all_listings(search_url)

# Get the text associated with every link
all_links = df_all_parameters['Link'].tolist()
all_text = get_text(all_links)

# Loop through every word on every page:
# If unique: add it to a dictionary
# Else: increment word counter
