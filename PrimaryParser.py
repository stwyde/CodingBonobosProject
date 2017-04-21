import newspaper
from newspaper import Article
import feedparser
NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")

class ParsedEntry:
    title = ""
    text = ""
    url = ""
    def __init__(self, name, body, link):
        self.url = link
        lowercaseText = body.lower()
        newStr = ""
        for c in lowercaseText:
            if c.isalpha():
                newStr+=c
        self.text = newStr
        self.title = name

for entry in NYTAmericas.entries:
    print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    parsedArticle = ParsedEntry(toParse.title, toParse.text, entry.link)
    print((parsedArticle.text))