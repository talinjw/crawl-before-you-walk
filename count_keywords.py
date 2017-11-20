import requests
import bs4
import operator
from pprint import pprint
from list_jobs import get_all_parameters_for_all_listings


def get_text_all(links):
    text_by_link = []

    for link in links:
        if 'http' in link:
            url = link
        else:
            url = 'https://' + link

        response = requests.get(url, timeout=5)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        all_text = soup.findAll(text=True)
        page_text = clean(all_text)
        text_by_link.append(page_text)

    return(text_by_link)


def get_text_from_link(link):
    if 'http' in link:
        url = link
    else:
        url = 'https://' + link

    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    all_text = soup.findAll(text=True)
    page_text = clean(all_text)

    return(page_text)


def clean(page_text):
    clean_text = []
    for text in page_text:
        if '\n' not in text and '/' not in text and len(text) > 2:
            clean_text.append(text.lower())

    return(clean_text)


def split_by_word(text_by_link):
    all_words = []
    for link_text in text_by_link:
        for text in link_text:
            words_in_text = text.split()
            for word in words_in_text:
                all_words.append(word)

    return(all_words)


def count_unique_words(list_of_words):
    unique_words = {}
    for word in list_of_words:
        if word not in unique_words:
            unique_words[word] = 1
        else:
            unique_words[word] = unique_words.get(word) + 1

    return(unique_words)


# Build search_query and get a dataframe containing all associated links
search_keyword = 'firefighter'
search_location = 'Bay Area, CA'
search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
search_url = 'https://www.indeed.com/' + search_query
print(search_url)

df_all_parameters = get_all_parameters_for_all_listings(search_url)

# Tokenize all text; generate list of words
all_links = df_all_parameters['Link'].tolist()
all_words = split_by_word(get_text_all(all_links))


# Create dictionary; word by frequency
words_to_frequency = count_unique_words(all_words)
sort_by_key = sorted(words_to_frequency.items(), key=operator.itemgetter(0))
pprint(sort_by_key)
# sort_by_val = sorted(words_to_frequency.items(), key=operator.itemgetter(1))
# pprint(sort_by_val)
