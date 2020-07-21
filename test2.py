import asyncio
import time
import aiohttp
import feedparser


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
    sites = [
        "https://rss.golem.de/rss.php?feed=ATOM1.0",
        "https://www.tagesschau.de/xml/rss2_https/",
    ]
    start_time = time.time()

    # Retrieve all elements from the listed feeds
    entries = asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")
