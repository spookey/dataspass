#!/usr/bin/env python3

from html.parser import HTMLParser
from ssl import PROTOCOL_SSLv23, SSLContext
from sys import exit as _exit
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class DataSpass(HTMLParser):
    __matched = False
    __result = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, values in attrs:
                if name == 'class' and all([
                        val in values for val in
                        ('volume', 'fit-text-to-container')
                ]):
                    self.__matched = True

    def handle_endtag(self, tag):
        if self.__matched and tag == 'div':
            self.__matched = False

    def handle_data(self, data):
        if self.__matched:
            self.__result.append(data.strip().rstrip('/'))

    def error(self, message):
        pass

    @property
    def result(self):
        return 'left: {}'.format(' of '.join(self.__result)).strip()


def main():
    parser = DataSpass()
    context = SSLContext(PROTOCOL_SSLv23)
    address = '?'.join([
        'https://datapass.de/home', urlencode({
            'continue': 'true',
        })
    ])

    try:
        with urlopen(address, context=context) as resp:
            html = resp.read().decode('utf-8')
            parser.feed(html)
    except URLError:
        return False

    print(parser.result)
    return True


if __name__ == '__main__':
    _exit(not main())
