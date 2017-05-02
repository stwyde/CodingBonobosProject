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
    tagTable = {}
    def __init__(self, name, body, link):
        self.url = link
        self.title = name
        #sanitizes text, sets everything to lowercase, removes numbers and symbols but keeps spaces leading to just words separated by spaces.
        lowercaseText = body.lower()
        newStr = ""
        for c in lowercaseText:
            if c.isalpha() or c==" ":
                newStr+=c
        self.text = newStr


        #creates dictionary with word occurances in the occurrenceTable dictionary object.
        wordsList = self.text.split()
        for word in wordsList:
            if word not in removeSet:
                if word not in self.tagTable.keys():
                    self.tagTable[word] = 0
                self.tagTable[word] = self.tagTable[word] + 1
            if word in removeSet:
                wordsList.remove(word)


        #standardizes tagList to be percentages
        wordCount = len(wordsList)
        for word in wordsList:
            self.tagTable[word] = self.tagTable[word] / wordCount

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
    print((parsedArticle.tagTable))
