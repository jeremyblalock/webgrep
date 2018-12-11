from HTMLParser import HTMLParser
from urlparse import urlparse, urlunparse

''' Returns the string with ansi excape color characters '''
def colorize(s, start = None, end = None):
    red = '\033[1;91m'
    endc = '\033[0m'
    #if start is end is None:
    #    return ''.join((red, s, endc))
    if start is None:
        start = 0
    if end is None:
        end = len(s)
    return s[:start] + red + s[start:end] + endc + s[end:]

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data().strip()

def get_link_url(url, link):
    u = urlparse(url)
    u2 = urlparse(link)
    
    scheme = u2.scheme
    netloc = u2.netloc
    path = u2.path
    query = u2.query
    params = u2.params
    fragment = u2.fragment
    username = u2.username
    password = u2.password
    hostname = u2.hostname
    port = u2.port

    if scheme == '':
        scheme = u.scheme
    if netloc == '':
        if len(path) == 0:
            return None
        elif path[0] != '/':
            p = u.path.split('/')
            d = '/'.join(p[:len(p) - 1]) + '/'
            path = d + path
        scheme = u.scheme
        netloc = u.netloc
    return urlunparse((scheme, netloc, path, params, query, fragment))

