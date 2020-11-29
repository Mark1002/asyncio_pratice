"""Demo for sync vs async."""
import requests
import asyncio
import aiohttp
from pyquery import PyQuery


def fetch_html_sync(word: str) -> list:
    """Fetch html sync."""
    url = f'http://www.zdic.net/zd/sw/bs/?bs={word}'
    res = requests.get(url)
    res.raise_for_status()
    dom = PyQuery(res.text)
    return dom('a').text().split()


def sync_fetch_word(words: list) -> list:
    """Sync fetch word."""
    sub_words = []
    for i, word in enumerate(words, 1):
        print(f'no.{i}: {word}')
        try:
            sub_words += fetch_html_sync(word)
        except Exception as e:
            print(f'error: {e}')
    sub_words = list(set(sub_words))
    return sub_words


def main():
    """Main."""
    with open('word.txt', 'r') as file:
        words = file.readlines()
    words = list(map(lambda x: x.replace('\n', ''), words))
    sub_words = sync_fetch_word(words)

    with open('sub_word.txt', 'w') as file:
        file.writelines(sub_words)


if __name__ == "__main__":
    main()
