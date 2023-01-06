import requests
import json
from db import Kattis
from bs4 import BeautifulSoup


CONTEST_URL = "https://open.kattis.com/past-contests"
PREFIX = "https://open.kattis.com"

def valid_contest(link):
    return link.startswith("/contests/")

def valid_problem(link):
    return valid_contest and 'problems' in link

def process_link(link):
    idx = link.find('/problems')
    problem_link = link[idx:]
    
    name = link.split('/')[-1]

    return (name, PREFIX + problem_link)

def get(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content

def difficulty(problem):
    page = BeautifulSoup(get(problem), 'lxml')
    metadata = page.find('span', class_='difficulty_number').text
    metadata = metadata.split('-')
    sm = 0
    for num in metadata:
        sm += float(num)
    diff = sm / len(metadata)
    print(diff)
    return diff


def update_problems(k):
    page = get(CONTEST_URL)
    bsoup = BeautifulSoup(page, 'lxml')
    atags = bsoup.find_all('a')
    contests = []
    for a in atags:
        try:
            link = a['href']
        except KeyError:
            continue
        if not valid_contest(link):
            continue
        contests.append(link)

    for contest in contests:
        page = get(f"{PREFIX}{contest}/problems")
        bsoup = BeautifulSoup(page, 'lxml')
        problems = bsoup.table
        if problems is None:
            continue
        atags = problems.find_all('a')
        for a in atags:
            link = a['href']
            if not valid_problem(link):
                continue
            name, full_link = process_link(link)
            diff = difficulty(full_link)
            k['problems'][name] = k['problems'].get(link, {})
            k['problems'][name]['diff'] = diff
            k['problems'][name]['url']  = full_link

def open_json(file):
    with open(file) as f:
        try:
            k = json.load(f)
        except:
            k = {}
            k['problems'] = {}
    return k

if __name__ == "__main__":
    k = open_json("kattis.json")
    update_problems(k)
    with open("kattis.json", 'w') as f:
        json.dump(k, f)