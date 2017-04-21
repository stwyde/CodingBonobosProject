import newspaper
from newspaper import Article
import feedparser
NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")

class ParsedEntry:
    title = ""
    text = ""
    url = ""
    occuranceTable = {}
    def __init__(self, name, body, link):
        self.url = link
        lowercaseText = body.lower()
        newStr = ""
        for c in lowercaseText:
            if c.isalpha() or c==" ":
                newStr+=c
        self.text = newStr
        self.title = name
        wordsList = self.text.split()
        for word in wordsList:
            if word not in self.occuranceTable.keys():
                self.occuranceTable[word] = 0
            self.occuranceTable[word] = self.occuranceTable[word] + 1



for entry in NYTAmericas.entries:
    print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    parsedArticle = ParsedEntry(toParse.title, toParse.text, entry.link)
    print((parsedArticle.occuranceTable))