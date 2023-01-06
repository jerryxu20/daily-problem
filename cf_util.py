import requests
from bs4 import BeautifulSoup

def get_problem_tags():
    res = requests.get("https://codeforces.com/problemset")
    bsoup = BeautifulSoup(res.content, 'lxml')
    tags = []
    for select in bsoup.find_all('option'):
        tag = select.text
        if not tag or '*' in tag:
            print(tag, "(skipped)")
            continue
        print(tag)
        tags.append(tag)
    print(tags)
    
if __name__ == "__main__":
    get_problem_tags()