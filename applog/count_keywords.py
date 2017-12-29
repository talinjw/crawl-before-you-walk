import requests
import bs4
import operator

from os import path
from list_jobs import get_all_parameters_for_all_listings
from pprint import pprint

debug = True

d = path.dirname(__file__)

with open(path.join(d, 'COMMON.txt')) as f1:
    COMMON = set(line.strip() for line in f1)

with open(path.join(d, 'EN_DICT.txt')) as f2:
    EN_DICT = set(line.lower().strip() for line in f2)

def get_text_all(links, max_links):
    # Provided a list of urls, get all text from each url
    text_by_link = []
    success_counter = 0
    failure_counter = 0

    if debug:
        total_number_of_links = len(links)
        print('Out of {} links in total...'.format(total_number_of_links))

    for link in links:
        if 'http' in link:
            url = link
        else:
            url = 'https://' + link

        try:
            response = requests.get(url, timeout=3)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            all_text = soup.findAll(text=True)
            page_text = all_text
            text_by_link.append(page_text)
            success_counter = success_counter + 1
            if success_counter == max_links:
                break
            
        except:
            if debug:
                print("{} did not work for some reason.".format(url))
            failure_counter = failure_counter + 1
            continue

    if debug:
        print('{} were crawled successfully.'.format(
                success_counter))

    return(text_by_link)


def get_text_from_link(link):
    # Provided a single url, get all text
    if 'http' in link:
        url = link
    else:
        url = 'https://' + link

    try:
        response = requests.get(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        all_text = soup.findAll(text=True)
        page_text = all_text

    except:
        if debug:
            print("{} did not work for some reason.".format(url))

    return(page_text)


def clean(word):
    # Removes punctuation and special chars from a specified string
    clean_word = ''.join(e for e in word.lower() if e.isalnum())
    return(clean_word)


def filter_by_relevance(words):
    # Exclude specific words and ensure all words are dict terms
    relevant_list = []

    with open(path.join(d, 'CUSTOM.txt')) as f3:
        CUSTOM = set(line.strip() for line in f3)
    
    for word in words:
        if len(word) < 12 and len(word) > 3 and \
           any(char.isdigit() for char in word) is False:
            if word not in COMMON and word not in CUSTOM:
                if word in EN_DICT:
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


def get_words_by_freq(sort_type, search_url, max_links):
    # Provided a search_string_url, return a dictionary containing words-b-freq
    df_all_parameters = get_all_parameters_for_all_listings(search_url)
    all_links = df_all_parameters['Link'].tolist()
    all_words = split_by_word(get_text_all(all_links, max_links))
    relevant_words = filter_by_relevance(all_words)
    words_by_freq = count_unique_words(relevant_words)

    print('Within the dictionary, there are {} unique words.'.format(
          len(words_by_freq)))

    if debug:
        if sort_type is 'key':
            sort_key = sorted(words_by_freq.items(), key=operator.itemgetter(0))
            pprint(sort_key)

        elif sort_type is 'value':
            sort_val = sorted(words_by_freq.items(), key=operator.itemgetter(1))
            pprint(sort_val)

        else:
            print('No sort key specified.')

    return(words_by_freq)


if __name__ == '__main__':

    # Build search_url and get a dataframe containing all associated links
    search_keyword = 'firefighter'
    search_location = 'Bay Area, CA'
    search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
    search_url = 'https://www.indeed.com/' + search_query
    print(search_url)

    get_words_by_freq(None, search_url, 5)
