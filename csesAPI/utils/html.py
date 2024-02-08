from lxml import html
from lxml.html import HtmlElement


def parse_html(html_string):
    try:
        parsed_html = html.fromstring(html_string)
    except:
        parsed_html = None

    return parsed_html


def to_string(element):
    return html.tostring(element).decode("utf-8")


def get_children(element):
    return element.getchildren()


def find(element, xpath):
    result = element.xpath(xpath)
    if result:
        return result[0]
    else:
        return None


def get_attribute(element: HtmlElement, attribute: str):
    return element.get(attribute)


def get_text(element: HtmlElement):
    return element.text_content()
