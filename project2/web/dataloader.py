import enum
import requests
import json
import random


API_HOST_ADDR = 'http://127.0.0.1:8080'


class ShowLevel(enum.Enum):
    ONLY_QA = 0
    WITH_NAME_SOME_FACT = 1
    WITH_NAME_FULL_FACT = 2


def generate_problems(count: int=16):
    problems = []
    
    showlevels = [ShowLevel(i % 3) for i in range(count)]

    for i in range(count):
        conf = 'low' if i < count // 2 else 'high'

        problem = json.loads(requests.get(f'{API_HOST_ADDR}/problem?level={conf}').text)
        problem['answer'] = problem['top5'][0]
        random.shuffle(problem['top5'])
        problems.append((problem, showlevels[i]))

    random.shuffle(problems)
    return problems
