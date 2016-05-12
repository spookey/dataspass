#!/usr/bin/env python3

from html.parser import HTMLParser
from urllib.request import urlopen


class DataSpass(HTMLParser):
    __matched = False
    result = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and [
            a for a in attrs if 'class' in a[0] and
                'barTextBelow' in a[-1]
        ]:
            self.__matched = True
        if tag == 'td' and [
            a for a in attrs if 'class' in a[0] and
                any([
                    all([
                        b in a[-1] for b in [c, 'infoValue']
                    ])
                ] for c in ['expiryTime', 'remainingTime'])
        ]:
            self.result.append(' ')
            self.__matched = True

    def handle_endtag(self, tag):
        if self.__matched and any([tag == a for a in ['div', 'td']]):
            self.__matched = False

    def handle_data(self, data):
        if self.__matched:
            self.result.append(data)


def main():
    parser = DataSpass()

    with urlopen('http://datapass.de/home?continue=true') as s:
        html = s.read().decode('utf-8')
        parser.feed(html)
    return ''.join(parser.result).strip()


if __name__ == '__main__':
    print(main(), end='')
