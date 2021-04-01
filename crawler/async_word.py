"""Demo for async."""
import asyncio
import aiohttp
import time
from aiohttp import ClientSession
from pyquery import PyQuery


async def fetch_html_async(word: str, session: ClientSession) -> list:
    """Async fetch html."""
    url = f'http://www.zdic.net/zd/sw/bs/?bs={word}'
    sub_words = []
    try:
        res = await session.request(method="GET", url=url)
        res.raise_for_status()
        html = await res.text()
        dom = PyQuery(html)
        sub_words = dom('a').text().split()
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        print(f'error: {e}')
    except Exception as e:
        print(f'error: {e}')
    return sub_words


async def async_fetch_word(words: list) -> list:
    """Async fetch word."""
    tasks = []
    sub_words = []
    async with ClientSession() as session:
        for i, word in enumerate(words, 1):
            print(f'no.{i}: {word}')
            tasks.append(fetch_html_async(word, session))
        results = await asyncio.gather(*tasks)
    for result in results:
        sub_words += result
    sub_words = list(set(sub_words))
    return sub_words


def main():
    """Main."""
    start_time = time.perf_counter()
    with open('word.txt', 'r') as file:
        words = file.readlines()
    words = list(map(lambda x: x.replace('\n', ''), words))
    sub_words = asyncio.run(async_fetch_word(words))
    print(f'total {len(sub_words)} words')
    with open('sub_word.txt', 'w') as file:
        file.writelines(sub_words)
    elapsed = time.perf_counter() - start_time
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    main()
