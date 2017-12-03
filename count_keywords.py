import requests
import bs4
import operator
import time
from list_jobs import get_all_parameters_for_all_listings
from pprint import pprint


def get_text_all(links):
    # Provided a list of urls, get all text from each url
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
        page_text = all_text
        text_by_link.append(page_text)
        time.sleep(1)
    return(text_by_link)


def get_text_from_link(link):
    # Provided a single url, get all text
    if 'http' in link:
        url = link
    else:
        url = 'https://' + link

    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    all_text = soup.findAll(text=True)
    page_text = all_text

    return(page_text)


def clean(word):
    # Removes punctuation and special chars from a specified string
    clean_word = ''.join(e for e in word.lower() if e.isalnum())
    return(clean_word)


def filter_by_relevance(words):
    # Exclude specific words and ensure all words are dict terms
    with open('/home/talin/projects/p_keywords/top1k.txt') as f1:
        top1k = set(line.strip() for line in f1)

    with open('/home/talin/projects/p_keywords/custom.txt') as f2:
        custom = set(line.strip() for line in f2)

    with open('/home/talin/projects/p_keywords/en_dict.txt') as f3:
        en_dict = set(line.lower().strip() for line in f3)

    relevant_list = []

    for word in words:
        if len(word) < 12 and len(word) > 3 \
         and any(char.isdigit() for char in word) is False:
                if word not in top1k and word not in custom:
                    if word in en_dict:
                        relevant_list.append(word)

    return(relevant_list)


def split_by_word(text_by_link):
    # Split chunks into words
    all_words = []
    for link_text in text_by_link:
        for text in link_text:
            words_in_text = text.split()
            for word in words_in_text:
                clean_word = clean(word)
                all_words.append(clean_word)

    return(all_words)


def count_unique_words(list_of_words):
    # Create a dictionary containing a list of words and their relative freq
    unique_words = {}
    for word in list_of_words:
        if word not in unique_words:
            unique_words[word] = 1
        else:
            unique_words[word] = unique_words.get(word) + 1

    return(unique_words)


if __name__ == '__main__':

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
    relevant_words = filter_by_relevance(all_words)

    # Create dictionary; word by frequency
    words_by_frequency = count_unique_words(relevant_words)

    # sort_key = sorted(words_by_frequency.items(), key=operator.itemgetter(0))
    # pprint(sort_key)
    sort_val = sorted(words_by_frequency.items(), key=operator.itemgetter(1))
    pprint(sort_val)
