from util import Codeforces, get
import json

URL = "https://codeforces.com/api/problemset.problems?"
TAGS = ['2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theorem', 'combinatorics',
        'constructive algorithms', 'data structures', 'dfs and similar', 'divide and conquer', 'dp', 'dsu',
        'expression parsing', 'fft', 'flows', 'games', 'geometry', 'graph matchings', 'graphs', 'greedy',
        'hashing', 'implementation', 'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory',
        'probabilities', 'schedules', 'shortest paths', 'sortings', 'string suffix structures', 'strings',
        'ternary search', 'trees', 'two pointers']

def construct_url(problem):
    contest_id = problem['contestId']
    letter = problem['index']
    return f"https://codeforces.com/contest/{contest_id}/problem/{letter}"

def update_problems(cf):
    for tag in TAGS:
        url = URL + f"?tags={tag}"
        url = url.encode()

        content = get(url)
        problems = json.loads(content)['result']['problems']

        if len(problems) == 0:
            print("no problems from {url}")
            continue

        data = []
        tag_data = []
        for p in problems:
            # name, url, website, contest_id, index, rating
            if "rating" not in p:
                continue
            name = p['name']
            tags = ",".join(p['tags'])
            p_url = construct_url(p)
            contest_id = str(p['contestId'])
            index = p['index']
            rating = p['rating']
            print(rating)
            data.append((name, p_url, "codeforces", contest_id, index, rating))
            tag_data.append((p_url, tags))
            
            if len(data) == 1:
                cf.insert(data, tag_data)
                data = []
                tag_data = []
        cf.insert(data, tag_data)

if __name__ == "__main__":
    cf = Codeforces('problems.db')
    update_problems(cf)
    cf.close_connection()