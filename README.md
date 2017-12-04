# You've Got To Crawl (Before You Walk)
A project to learn Python3 and some web development; crawls indeed.com to enable interesting analysis on job listings.

![](/test.png?raw=true "Example output post-query; this spider was created from the search term 'firefighter' and location 'bay area.'")

1. Allows the user to search by keyword/location via form; outputs all listing parameters to an HTML table (optionally CSV).
2. Allows the user to search by keyword/location via form; outputs the results of this analysis to a word cloud based on frequency.

Uses a number of third-party libraries, including:
- requests
- bs4
- flask
- pandas
- wordcloud

See requirements.txt for a list of all dependencies.
