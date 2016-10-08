import urllib2
from bs4 import BeautifulSoup
from sources import HtmlSource


class ConfigSource(HtmlSource):
    def check_content(self, i, tokens, mycontent):
        results = []
        print tokens[i], 'starting'
        for content in mycontent.find_all(tokens[i]):
            i += 1

            runner = True
            while tokens[i] == ',' or tokens[i] == '(':
                print tokens[i + 1]
                print tokens[i + 2]
                print content.get(tokens[i + 1])
                print tokens[i + 3]
                print '------'

                if tokens[i + 3] == 'x':
                    results += content.get(tokens[i + 1])
                    print "angekommen"
                    print content.get(tokens[i + 1])

                # and content.get(tokens[i+2]) == "=" )):
                if (not(content.get(tokens[
                        i + 1]) == tokens[i + 3])):
                    runner = False
                    print 'not ok'
                else:
                    print 'ok'
                i += 4
            print i
            if tokens[i] == ')':
                print "da"
                if runner and i < len(tokens):
                    print "finale"

                    results += self.check_content(i + 1, tokens, content)
            else:
                raise Exception('Klammer zu vergessen')
        return results

    def process_line(self, line):
        tokens = line.split(' ')
        print tokens
        soup = self.get_soup(line)
        i = 1
        self.check_content(i, tokens, soup)

    def get_soup(self, url):
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        html_doc = urllib2.urlopen(req)
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def __init__(self):
        print 'hi'

def main():
    src = ConfigSource()
    src.process_line('http://www.xkcd.com/ div ( id = comic ) img ( src = x )')

if __name__ == "__main__":
    main()

##f = open('testCFG.txt', 'r')
# for line in f:
# process_line(line)
