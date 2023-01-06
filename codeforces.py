from bs4 import BeautifulSoup
import requests
import random
import json
import math

URL = "https://codeforces.com/api/problemset.problems?"
TAGS = ['2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theorem', 'combinatorics',
        'constructive algorithms', 'data structures', 'dfs and similar', 'divide and conquer', 'dp', 'dsu',
        'expression parsing', 'fft', 'flows', 'games', 'geometry', 'graph matchings', 'graphs', 'greedy',
        'hashing', 'implementation', 'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory',
        'probabilities', 'schedules', 'shortest paths', 'sortings', 'string suffix structures', 'strings',
        'ternary search', 'trees', 'two pointers']


def rand(a, b):
    # Random int in the range [a, b)
    return math.floor(random.random() * (b - a)) + a


def construct_url(problem):
    contest_id = problem['contestId']
    letter = problem['index']
    return f"https://codeforces.com/contest/{contest_id}/problem/{letter}"


def open_json(file):
    with open(file) as f:
        try:
            k = json.load(f)
        except:
            k = {}
            k['contest'] = {}
    return k


def dump_json(dict):
    with open('cf.json', 'w') as f:
        json.dump(dict, )
    return


def update_problems(k):
    cf = open_json('cf.json')
    for tag in TAGS:
        url = URL + f"?tags={tag}"
        url = url.encode()

        res = requests.get(url)
        problems = json.loads(res.content)['result']['problems']

        if len(problems) == 0:
            continue

        for p in problems:
            p_url = construct_url(p)
            contest = p['contestId']
            index = p['index']

            cf['contest'][contest] = cf['contest'].get(contest, {})
            if index in cf['contest'][contest]:
                continue

            p['used'] = False
            cf['contest'][contest][index] = p

    dump_json(cf)


def get_problem():
    problems = []
    for contest in cf['contest']:
        pass


if __name__ == "__main__":
    cf = {"contest": {"1244": {"D": {"contestId": 1244, "index": "D", "name": "Paint the Tree", "type": "PROGRAMMING", "points": 1750.0,
                                     "rating": 1800, "tags": ["brute force", "constructive algorithms", "dp", "graphs", "implementation", "trees"]}}}}
    problems = []
    for contest in cf['contest'].values():
        for problem in contest.values():
            print(problem)
