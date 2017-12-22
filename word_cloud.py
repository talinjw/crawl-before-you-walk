import numpy as np
# import random

from os import path
from PIL import Image
from wordcloud import WordCloud
from count_keywords import get_words_by_freq


# def gry(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(10, 50)


if __name__ == '__main__':

    # Build a search_url and get a dict containing words and their freq
    search_keyword = 'firefighter'
    search_location = 'Bay Area, CA'
    search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
    search_url = 'https://www.indeed.com/' + search_query
    print(search_url)

    d_words_by_frequency = get_words_by_freq(None, search_url)

    # Setup mask
    d = path.dirname(__file__)

    with Image.open(path.join(d, 'static/images/data-spider-mask.png')) as img:
        new_image = Image.new('RGB', img.size, (255, 255, 255))
        new_image.paste(img, img)
        mask = np.array(new_image)

    # Setup WordCloud
    font_path = path.join(d, 'app/static/site/DIN_Condensed_Bold.ttf')

    wc = WordCloud(font_path=font_path,
                   background_color="white",
                   max_words=2000,
                   mask=mask,
                   max_font_size=300,
                   random_state=42)

    # Generate WordCloud
    wc.generate_from_frequencies(d_words_by_frequency)
    # wc.recolor(color_func=gry, random_state=3)
    wc.to_file("test.png")
