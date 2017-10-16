# Crawl-Indeed
Crawls indeed.com to enable interesting analysis on job listings by keyword and location. 

1. Allows the user to search by keyword/location via form; collects all listing parameters; outputs all listing parameters to an HTML table (optionally, CSV).
2. Allows the user to search by keyword/location via form; collects the urls to all job postings; loops through the urls and stores all page text as an item within a list; counts all unique keyterms within the list; outputs the results of this analysis to an HTML table ordered by frequency.

Uses a number of third-party modules, including:
- requests
- bs4
- flask

See requirements.txt for a list of all dependencies.
