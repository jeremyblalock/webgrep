import utils, re, urllib2, math, sys
from bs4 import BeautifulSoup

class FileParser(object):

    class MatchObj(object):
        def __init__(self, s, start, end):
            self.string = s
            self.start = start
            self.end = end
            self.pos = start, end
        def get(self):
            return self.string, self.start, self.end
        def colorize(self):
            try:
                return utils.colorize(self.string, self.start, self.end)
            except:
                return self.string
        def __str__(self):
            l = 70
            if len(self.string) > l:
                if self.end - self.start >= l:
                    self.string = self.string[self.start:self.end]
                    self.start, self.end = 0, len(self.string)
                else:
                    l -= 6
                    edges = (l - (self.end - self.start)) / 2.0
                    before, after = int(math.floor(edges)), int(math.ceil(edges))
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
                    s = self.string[self.start - before:self.end + after]
                    self.start = before + len(pre)
                    self.end = len(s) - after + len(pre)
                    self.string = pre + s + aft

            return self.colorize().encode('utf-8')

    def __init__(self, url):
        self.url = url
        self.retrieve(url)
        self.soup = BeautifulSoup(self.raw)

    def retrieve(self, url):
        try:
            u = urllib2.urlopen(url)
            tmp = u.read()
            #tmp = repr(tmp) #unicode(tmp.strip(codecs.BOM_UTF8), 'utf-8')
            self.raw = tmp
        except:
            self.raw = ''

    def search(self, pattern):
        body = self.soup.find('body')
        try:
            lines = body.prettify().split('\n')
        except:
            return []
        matches = []
        p = re.compile(pattern)
        for line in lines:
            line2 = utils.strip_tags(line)
            m = p.search(line2)
            if m:
                start = m.start()
                match_obj = FileParser.MatchObj(line2, start, start + len(m.group(0)))
                matches.append(match_obj)
        return matches

    def outlinks(self):
        body = self.soup.find('body')
        links = self.soup.findAll('a')
        urls = []
        for l in links:
            try:
                url = utils.get_link_url(self.url, l['href'])
                urls.append(url)
            except:
                pass
        return urls

