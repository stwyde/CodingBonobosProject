from nltk.corpus import stopwords
from newspaper import Article
import feedparser
NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")
removeSet = set(stopwords.words('english'))
class ParsedEntry:
    """Not called article to avoid conflict with Newspaper package"""
    title = ""
    text = ""
    url = ""
    occurrenceTable = {}
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
            if word not in removeSet:
                if word not in self.occurrenceTable.keys():
                    self.occurrenceTable[word] = 0
                self.occurrenceTable[word] = self.occurrenceTable[word] + 1

class tag:
    """Stores all information about a given tag, including lists of which articles
have the tag and the number of times the keywork appears in each."""
    def __init__(self, name):
        self.name = name
        self.taggedArticles = []

    def setArticles(self, articles):
        self.taggedArticles.append(articles)

for entry in NYTAmericas.entries:
    print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    parsedArticle = ParsedEntry(toParse.title, toParse.text, entry.link)
    print((parsedArticle.occurrenceTable))
