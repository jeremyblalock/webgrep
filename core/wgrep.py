import argparse, sys
from parser import FileParser

class Grepper(object):

    visited = []

    ''' Standard init function '''
    def __init__(self, color = False, depth = 1):
        self.color = color
        self.depth = depth

    ''' Returns the string with ansi excape color characters '''
    @staticmethod
    def colorize(s):
        red = '\033[91m'
        end = '\033[0m'
        return ''.join((red, s, end))

    ''' The main function, takes PATTERN and URL arguments, and
        prints the lines matching the query pattern. '''
    def grep(self, pattern, url, depth = -1):
        if depth is -1:
            depth = self.depth
        elif depth is 0 or not url or url in self.visited:
            return
        self.visited.append(url)
        f = FileParser(url)
        matches = f.search(pattern)
        if len(matches) > 0:
            print url + ':'
        for i in matches:
            print "    ", i
        if depth > 1:
            for i in f.outlinks():
                self.grep(pattern, i, depth - 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(sys.argv[0],
        description = "A tool to search ('grep') websites as you would a local directory")
    parser.add_argument('--color', action = 'store_const', const = True, default = False)
    parser.add_argument('-d', '--depth', default = 1)
    parser.add_argument('pattern')
    parser.add_argument('url')
    args = parser.parse_args()

    grepper = Grepper(color = args.color, depth = int(args.depth))
    grepper.grep(args.pattern, args.url)
    print 

