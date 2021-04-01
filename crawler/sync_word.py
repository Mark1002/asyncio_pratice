"""Demo for sync."""
import requests
import time
from pyquery import PyQuery


def fetch_html_sync(word: str) -> list:
    """Fetch html sync."""
    url = f'http://www.zdic.net/zd/sw/bs/?bs={word}'
    sub_words = []
    try:
        res = requests.get(url)
        res.raise_for_status()
        dom = PyQuery(res.text)
        sub_words = dom('a').text().split()
    except Exception as e:
        print(f'error: {e}')
    return sub_words


def sync_fetch_word(words: list) -> list:
    """Sync fetch word."""
    sub_words = []
    for i, word in enumerate(words, 1):
        print(f'no.{i}: {word}')
        sub_words += fetch_html_sync(word)
    sub_words = list(set(sub_words))
    return sub_words


def main():
    """Main."""
    start_time = time.perf_counter()
    with open('word.txt', 'r') as file:
        words = file.readlines()
    words = list(map(lambda x: x.replace('\n', ''), words))
    sub_words = sync_fetch_word(words)
    print(f'total {len(sub_words)} words')
    with open('sub_word.txt', 'w') as file:
        file.writelines(sub_words)
    elapsed = time.perf_counter() - start_time
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    main()
