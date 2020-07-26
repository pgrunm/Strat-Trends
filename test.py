import asyncio
import json
import logging
import time
from newspaper import Article
import sqlite3

import aiohttp
import feedparser
import newspaper as n
from ratelimit import limits, sleep_and_retry
from urllib.parse import urlparse


async def download_site(url):
    # async with session.get(url) as response:
    #     print("Read {0} from {1}".format(response.content_length, url))
    return feedparser.parse(url)


async def download_all_sites(sites):
    tasks = []
    for url in sites:
        task = asyncio.ensure_future(download_site(url))
        tasks.append(task)
    liste = await asyncio.gather(*tasks, return_exceptions=True)
    return liste


@sleep_and_retry
@limits(calls=5, period=1)
async def download_article(entry, source_id):
    article = Article(entry['link'], fetch_images=False, language='de')
    article.download()
    article.parse()

    # Parse the keywords
    # article.nlp()

    article.text.replace("'", "")

    # We need the entry, the content, the title and keywords.
    return (article.text, source_id, entry['link'], entry['title'])


async def download_articles(article_list, postmortem_titles, feed_url_dict):
    # List to return
    tasks = []

    # Iterateover all the feeds
    for feed in article_list:
        # Access the entries within each feed
        for entry in feed['entries']:
            # Prepare the foreign key of the source id
            source_id = feed_url_dict[feed.href]
            # Check if the title is within our database, if not download and save the postmortem.
            if entry['title'] not in postmortem_titles:
                logging.debug(
                    f"Article {entry['title']} not in database, downloading it from {entry['link']}")
                # Download the article
                tasks.append(asyncio.ensure_future(
                    download_article(entry, source_id)))

            # We need the url, the content, the title and keywords. But watch out, keywords may be an empty list!
    return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":

    # DB Connection
    conn = sqlite3.connect('postmortem.db', check_same_thread=False)
    c = conn.cursor()

    # Logging Handler
    # Configure logging
    logging.basicConfig(handlers=[logging.FileHandler(filename='app.log', mode='w', encoding='utf-8')],
                        level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    example_url = 'http://127.0.0.1:8020/blog'
    d = feedparser.parse(example_url)
    if d['bozo'] != 1:
        # HTTP Status Code loggen...
        logging.debug(f'HTTP Status Code der Feed Abfrage ist {d["status"]}')

        if d['status'] == 200:
            # HTTP Status Code loggen
            logging.info('HTTP Status ist 200')

            # Gehe durch die Feed Einträge.
            for x in d['entries']:
                # print(json.dumps(x, indent=4, sort_keys=True))
                print(x['title'])
                print(x['link'])
            '''
            Offen:
            URL-ID
            Zeitpunkt des Abrufs (SQLite)
            Primary ID erzeugen

            Erledigt:
            feed.title
            feed.link
            '''
        else:
            logging.info(f'HTTP Status ist {d["status"]}')

    # Async stuff
    sites = [
        "https://rss.golem.de/rss.php?feed=ATOM1.0",
        "https://www.tagesschau.de/xml/rss2_https/",
    ]
    start_time = time.time()

    # Retrieve all elements from the listed feeds
    feeds = asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

    c.execute('select title from Postmortems;')

    # Fetch all postmortem title rows
    try:
        postmortem_titles = c.fetchall()
        logging.debug(f'Query returned: {postmortem_titles}')
    except sqlite3.Error as sqlite_error:
        logging.critical(
            f'Error occured while retrieving all rows: {sqlite_error}')

    # Need a dictionary to determine what site has which id
    feed_url_dict = dict()
    c.execute('select source_id, url from Sources;')
    try:
        feed_urls = c.fetchall()
        logging.debug(f'Query returned: {feed_urls}')
    except sqlite3.Error as sqlite_error:
        logging.critical(
            f'Error occured while retrieving all rows: {sqlite_error}')

    # Fill the dictionary
    for source_id, url in feed_urls:
        logging.debug(f'Adding the url {url} as key for source id {source_id}')
        feed_url_dict[url] = source_id

    articles = asyncio.get_event_loop().run_until_complete(
        download_articles(feeds, postmortem_titles, feed_url_dict))
    print(
        f"Downloaded {len(articles)} articles in {time.time() - start_time} seconds")

    # Save the data to the database
    try:
        c.executemany(
            'INSERT INTO Postmortems (content, fk_source_id, url, title) VALUES (?,?,?,?);', articles)
        conn.commit()
    except sqlite3.Error as sqlite_error:
        logging.critical(
            f'Error occured while inserting rows: {sqlite_error}')

    print(
        f"Finished in {time.time() - start_time} seconds")
    conn.close()

    # content, fk_source_id, pm_id, url, title
    for content, fk_source_id, url, title in articles:
        logging.info(
            f"INSERT INTO Postmortems (content, fk_source_id, url, title) VALUES ('{content}', {fk_source_id}, '{url}', '{title}');")
