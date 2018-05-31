#!/usr/bin/env python3

from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class DataSpass(HTMLParser):
    __matched = False
    __result = list()

    def handle_starttag(self, tag, attrs):
        if tag in ('div', 'td'):
            for name, values in attrs:
                if name == 'class' and any([
                        val in values for val in
                        ('barTextBelow', 'remainingTime', 'expiryTime')
                ]):
                    self.__matched = True

    def handle_endtag(self, tag):
        if self.__matched and tag in ('div', 'td'):
            self.__matched = False

    def handle_data(self, data):
        if self.__matched:
            self.__result.append(data.strip())

    def error(self, message):
        pass

    @property
    def result(self):
        return ' '.join(self.__result).strip()


def main():
    parser = DataSpass()
    address = '?'.join([
        'http://datapass.de/home', urlencode({
            'continue': 'true', 'lang': 'en'
        })
    ])

    try:
        with urlopen(address) as resp:
            html = resp.read().decode('utf-8')
            parser.feed(html)
    except URLError:
        return False

    print(parser.result)
    return True


if __name__ == '__main__':
    exit(not main())
