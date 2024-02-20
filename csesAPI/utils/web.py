import sys
from .html import parse_html, find, get_children, get_attribute, get_text, to_string
from .func import execution_time
from requests import get, session


CATEGORY_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/h2[ID]'
PROBLEMS_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/ul[ID]'

SOLVED_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[1]/td[2]'
ATTEMPTED_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[2]/td[2]'
SUCCESS_RATE_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[3]/td[2]'

TIME_LIMIT_XPATH = '/html/body/div[2]/div[2]/div[1]/ul/li[1]/text()'
MEMORY_LIMIT_XPATH = '/html/body/div[2]/div[2]/div[1]/ul/li[2]/text()'

PROBLEM_STATEMENT_XPATH = '/html/body/div[2]/div[2]/div[1]/div'


class CSESClient:
    _cookies = dict()

    @staticmethod
    def add_cookie(name, value):
        CSESClient._cookies[name] = value

    @staticmethod
    def remove_cookie(name):
        CSESClient._cookies.pop(name)

    @staticmethod
    def clear_cookies():
        CSESClient._cookies.clear()

    @staticmethod
    def get(*args, **kwargs):
        return get(*args, cookies=CSESClient._cookies, **kwargs)

    @staticmethod
    def retrieve_problems():
        tree = CSESClient.parse_url('https://cses.fi/problemset/')
        result = []

        for i in range(2, sys.maxsize):  # using sys.maxsize for an unbounded loop
            try:
                category = get_text(find(tree, CATEGORY_XPATH_TEMPLATE.replace('ID', str(i))))
                problems = find(tree, PROBLEMS_XPATH_TEMPLATE.replace('ID', str(i)))

                for child in get_children(problems):
                    href = get_attribute(find(child, 'a'), 'href')
                    url = f'https://cses.fi{href}'
                    _id = href.split('/')[-1]
                    title = get_text(find(child, 'a'))
                    stats = get_text(find(child, 'span'))
                    solved, attempts = map(int, stats.split('/'))

                    result.append({
                        'id': _id,
                        'title': title,
                        'url': url,
                        'category': category,
                        'solved_count': solved,
                        'attempted_count': attempts,
                    })
            except:
                break

        return result

    @staticmethod
    def retrieve_problem_stats(problem_id: str | int):
        tree = CSESClient.parse_url(f'https://cses.fi/problemset/task/{problem_id}/')

        solved = find(tree, SOLVED_XPATH)
        attempted = find(tree, ATTEMPTED_XPATH)
        success_rate = find(tree, SUCCESS_RATE_XPATH)

        if solved is None or attempted is None or success_rate is None:
            return None

        return {
            'solved': int(get_text(solved)),
            'attempted': int(get_text(attempted)),
            'success_rate': round(float(get_text(success_rate).replace('%', '')) / 100, 4)
        }

    @staticmethod
    @execution_time(time_unit='ms')
    def retrieve_problem_statement(problem_id: str | int):
        tree = CSESClient.parse_url(f'https://cses.fi/problemset/task/{problem_id}/')

        statement = find(tree, PROBLEM_STATEMENT_XPATH)

        if statement is None:
            return None

        children = get_children(statement)
        i = 0

        statement_parts, input_parts, output_parts = [], [], []
        parts = [statement_parts, input_parts, output_parts]
        for part in parts:
            while i < len(children) and children[i].tag != 'h1':
                part.append(to_string(children[i]))
                i += 1
            i += 1

        constraints_parts = [get_text(item) for item in get_children(children[i])]

        i += 3

        example_input, example_output = [], []
        example_parts = [example_input, example_output]
        for part in example_parts:
            while i < len(children) and children[i].tag == 'pre':
                part.append(get_text(children[i]))
                i += 1
            i += 1

        return {
            'statement': '\n'.join(statement_parts).replace('src="/', 'src="https://cses.fi/'),
            'input_format': '\n'.join(input_parts),
            'output_format': '\n'.join(output_parts),
            'constraints': '\n'.join(constraints_parts),
            'example_input': '\n'.join(example_input),
            'example_output': '\n'.join(example_output),
            **CSESClient.retrieve_problem_limits(tree)
        }

    @staticmethod
    def retrieve_problem_limits(tree):
        time_limit = find(tree, TIME_LIMIT_XPATH)
        memory_limit = find(tree, MEMORY_LIMIT_XPATH)

        if time_limit is None or memory_limit is None:
            return None

        time_limit = time_limit.strip()
        memory_limit = memory_limit.strip()

        time_limit = int(float(time_limit.split(' ')[0]) * 1000)
        memory_limit = int(memory_limit.split(' ')[0])

        return {
            'time_limit': time_limit,
            'memory_limit': memory_limit
        }

    @staticmethod
    def parse_url(url):
        response = CSESClient.get(url)

        if response.status_code != 200:
            return None

        source = get(url, cookies=CSESClient._cookies).content.decode('utf-8')

        tree = parse_html(source)

        return tree


if __name__ == '__main__':
    CSESClient.add_cookie('PHPSESSID', '2dee5f109ca1963720111c82758bed9196b21ab9')
    problem_statement = CSESClient.retrieve_problem_statement(1071)
    print(problem_statement)
