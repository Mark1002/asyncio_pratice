import requests
from pyquery import PyQuery

with open('word.txt', 'r') as file:
    words = file.readlines()

words = list(map(lambda x: x.replace('\n', ''), words))
sub_words = []

for i, word in enumerate(words, 1):
    print(f'no.{i}: {word}')
    url = f'http://www.zdic.net/zd/sw/bs/?bs={word}'
    try:
        res = requests.get(url)
        dom = PyQuery(res.text)
        sub_words += dom('a').text().split()
    except Exception as e:
        print(e)

sub_words = list(set(sub_words))

with open('sub_word.txt', 'w') as file:
    file.writelines(sub_words)
