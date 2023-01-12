from datetime import date
from util import rand_prob
import json

def open_config():
    try:
        with open('daily_problem.json') as f:
            p = json.load(f)
    except:
        p = {}
    return p

def save_config(p):
    with open('daily_problem.json', 'w') as f:
        json.dump(p, f)

if __name__ == "__main__":
    d = str(date.today())
    problems = open_config()
    if d not in problems:
        p1 = rand_prob("kattis")
        p2 = rand_prob("codeforces")
        problems[d] = [p1, p2]
        save_config(problems)
    print(problems[d])
    