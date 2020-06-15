import newspaper as n
import feedparser
import json
import logging

if __name__ == "__main__":

    # Logging Handler
    # Configure logging
    logging.basicConfig(format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.DEBUG, filemode='w', filename='app.log')

    example_url = 'http://127.0.0.1:8020/blog'
    d = feedparser.parse(example_url)

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
