from .html import parse_html, find, get_children, get_attribute, get_text
from requests import get, session


CATEGORY_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/h2[ID]'
PROBLEMS_XPATH_TEMPLATE = '/html/body/div[2]/div[2]/div/ul[ID]'

SOLVED_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[1]/td[2]'
ATTEMPTED_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[2]/td[2]'
SUCCESS_RATE_XPATH = '/html/body/div[2]/div[2]/div[1]/table[1]/tr[3]/td[2]'


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

        url = 'https://cses.fi/problemset/list/'

        source = CSESClient.get(url).content.decode('utf-8')

        tree = parse_html(source)

        categories = list()
        i = 2
        while True:
            try:
                category = get_text(find(tree, CATEGORY_XPATH_TEMPLATE.replace('ID', str(i))))
                problems = find(tree, PROBLEMS_XPATH_TEMPLATE.replace('ID', str(i)))
                for child in get_children(problems):
                    href = get_attribute(find(child, 'a'), 'href')
                    url = f'https://cses.fi{href}'
                    _id = href.split('/')[-1]
                    title = get_text(find(child, 'a'))
                    categories.append({'id': _id, 'title': title, 'url': url, 'category': category})
                i += 1
            except:
                break
        return categories

    @staticmethod
    def retrieve_problem_stats(problem_id: str | int):
        if not isinstance(problem_id, int) and not (isinstance(problem_id, str) and problem_id.isnumeric()):
            raise ValueError('Problem ID must be an integer or a string representing an integer')

        if isinstance(problem_id, str):
            problem_id = int(problem_id)

        url = f'https://cses.fi/problemset/stats/{problem_id}/'

        response = CSESClient.get(url)

        if response.status_code != 200:
            return None

        source = get(url, cookies=CSESClient._cookies).content.decode('utf-8')

        tree = parse_html(source)

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


if __name__ == '__main__':
    CSESClient.add_cookie('PHPSESSID', '2dee5f109ca1963720111c82758bed9196b21ab9')
    problems = CSESClient.retrieve_problems()
    print(problems)
    print(CSESClient.retrieve_problem_stats(1068))
