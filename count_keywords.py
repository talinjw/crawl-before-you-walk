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
        page_text = all_text
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
    page_text = all_text

    return(page_text)


def clean(word):
    clean_word = ''.join(e for e in word.lower() if e.isalnum())
    return(clean_word)

    
def filter_by_property(word):
    if len(word) > 20 or len(word) < 2 or any(char.isdigit() for char in word) == True:
        return False
    else:
        return True

def filter_by_word(list_of_words):
 


def split_by_word(text_by_link):
    all_words = []
    for link_text in text_by_link:
        for text in link_text:
            words_in_text = text.split()
            for word in words_in_text:
                clean_word = clean(word)
                if filter_by_property(clean_word) == True:
                    all_words.append(clean_word)

    return(all_words)


def count_unique_words(list_of_words):
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


    # Create dictionary; word by frequency
    words_by_frequency = count_unique_words(all_words)
    sort_key = sorted(words_by_frequency.items(), key=operator.itemgetter(0))
    pprint(sort_key)
    print(len(sort_key))
    
    # sort_val = sorted(words_by_frequency.items(), key=operator.itemgetter(1))
    # pprint(sort_val)
