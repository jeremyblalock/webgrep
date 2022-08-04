''' Various utils to help with parsing '''
from html.parser import HTMLParser
from urllib.parse import urlparse, urlunparse


def colorize(string, start=None, end=None):
    ''' Returns the string with ansi excape color characters '''
    red = '\033[1;91m'
    endc = '\033[0m'

    if start is None:
        start = 0
    if end is None:
        end = len(string)
    return string[:start] + red + string[start:end] + endc + string[end:]


class MLStripper(HTMLParser):
    ''' Strip out HTML '''
    def __init__(self):
        print("INITILIZING MLStripper")
        super(MLStripper, self).__init__()
        self.fed = []
        self.position = []

    def handle_starttag(self, tag, attrs):
        print('START TAG:' + tag)
        self.position.append(tag)
        print(self.position)

    def handle_endtag(self, tag):
        print('END TAG:' + tag, self.position)
        self.position.pop()

    def handle_data(self, data):
        ''' Append data to buffer '''
        current_tag = self.position[-1] if len(self.position) > 0 else None

        if current_tag in ('style', 'script'):
            return

        self.fed.append(data)

    def get_data(self):
        ''' Return the data stored '''
        return ''.join(self.fed)


def strip_tags(html):
    ''' Remove HTML Tags '''
    print('>>>>>>>>>>>>>>>>', html)
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data().strip()


def get_link_url(base_url, link_href):
    ''' Get the URL of a link element '''
    url1 = urlparse(base_url)
    url2 = urlparse(link_href)

    scheme = url2.scheme
    netloc = url2.netloc
    path = url2.path
    query = url2.query
    params = url2.params
    fragment = url2.fragment
    # username = u2.username
    # password = u2.password
    # hostname = u2.hostname
    # port = u2.port

    if scheme == '':
        scheme = url1.scheme
    if netloc == '':
        if len(path) == 0:
            return None

        elif path[0] != '/':
            p = url1.path.split('/')
            d = '/'.join(p[:len(p) - 1]) + '/'
            path = d + path

        scheme = url1.scheme
        netloc = url1.netloc

    return urlunparse((scheme, netloc, path, params, query, fragment))
