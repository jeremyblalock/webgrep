''' File Parser '''

# import codecs
import math
import re
# import sys
# import urllib
import urllib.request as urllib2
from bs4 import BeautifulSoup

from html5lib.html5parser import parse
from html5lib.serializer import serialize

from .utils import strip_tags, get_link_url, colorize


class FileParser():
    ''' File Parser '''

    class MatchObj():
        ''' A single match '''

        def __init__(self, s, start, end):
            self.string = s
            self.start = start
            self.end = end
            self.pos = start, end

        def get(self):
            ''' Get the match string & position '''
            return self.string, self.start, self.end

        def colorize(self):
            ''' Get the colorized version of string '''
            try:
                return colorize(self.string, self.start, self.end)
            except:
                return self.string

        def __str__(self):
            length = 70

            if len(self.string) > length:
                if self.end - self.start >= length:
                    self.string = self.string[self.start:self.end]
                    self.start, self.end = 0, len(self.string)
                else:
                    length -= 6
                    edges = (length - (self.end - self.start)) / 2.0
                    before = int(math.floor(edges))
                    after = int(math.ceil(edges))

                    pre = aft = "..."
                    if self.start < before:
                        pre = ''
                        after += before - self.start
                        before = self.start
                    elif len(self.string) - self.end < after:
                        aft = ''
                        piece = (len(self.string) - self.end)
                        before += after - piece
                        after = piece

                    string = self.string[self.start - before:self.end + after]
                    self.start = before + len(pre)
                    self.end = len(string) - after + len(pre)
                    self.string = pre + string + aft

            return self.colorize()

    def __init__(self, url):
        self.url = url
        self.retrieve(url)
        self.clean_raw()
        self.soup = BeautifulSoup(self.raw, features='html5lib')

    def retrieve(self, url):
        ''' Retrieve page at the specified URL '''
        try:
            socket = urllib2.urlopen(url)
            tmp = socket.read()
            # tmp = repr(tmp) #unicode(tmp.strip(codecs.BOM_UTF8), 'utf-8')
            self.raw = tmp
        except:
            self.raw = ''

    def clean_raw(self):
        ''' Clean page content '''
        # parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
        html5lib_object = parse(self.raw)
        output_generator = serialize(html5lib_object, omit_optional_tags=False)

        html_string = ''.join(list(output_generator))

        self.raw = html_string

    def search(self, pattern, ignore_case):
        ''' Search for pattern '''
        body = self.soup.find('body')

        try:
            lines = body.prettify().split('\n')
        except:
            return []

        matches = []

        if ignore_case:
            pattern = re.compile(pattern.lower())
        else:
            pattern = re.compile(pattern)

        for line in lines:
            line2 = strip_tags(line)

            if ignore_case:
                line2 = line2.lower()

            p_match = pattern.search(line2)

            if p_match:
                start = p_match.start()

                match_obj = FileParser.MatchObj(
                    line2, start, start +
                    len(p_match.group(0)))

                matches.append(match_obj)
        return matches

    def outlinks(self):
        ''' Get outbound links from page '''
        links = self.soup.findAll('a')
        urls = []

        for link in links:
            try:
                url = get_link_url(self.url, link['href'])
                urls.append(url)
            except:
                pass
        return urls
