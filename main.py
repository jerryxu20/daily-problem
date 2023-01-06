from datetime import date
import json

def open_config():
    try:
        with open('daily_problem.json') as f:
            p = json.dump(f)
    except:
        p = {}
    return p

if __name__ == "__main__":
    d = str(date.today())
    problems = open_config()
    print(problems)
    if d not in problems:
        p1 = rand_prob()
        p2 = rand_prob()
        problems[d] = [p1, p2]
    print(problems[d])