from util import Kattis, get
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

    data = []
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

            data.append((name, full_link, "kattis", diff))
            if len(data) == 10:
                k.insert(data)
                data = []
    k.insert(data)

if __name__ == "__main__":
    k = Kattis('problems.db')
    update_problems(k)
    k.close_connection()
