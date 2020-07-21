import asyncio
import json
import logging
import time

import aiohttp
import feedparser
import newspaper as n


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
    # print(liste)

    return liste


if __name__ == "__main__":

    # Logging Handler
    # Configure logging
    logging.basicConfig(format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.DEBUG, filemode='w', filename='app.log')

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

    # Iterateover all the feeds
    for feed in feeds:
        # Access the entries within each feed
        for entry in feed['entries']:
            # Access the data within the entry like title or author.
            print(entry)
