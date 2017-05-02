from nltk.corpus import stopwords
from newspaper import Article
import feedparser
NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")
removeSet = set(stopwords.words('english'))
class ParsedEntry:
    #Not called article to avoid conflict with Newspaper package
    def __init__(self, name, body, link):
        self.tagTable = {}
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
            if word in removeSet:
                wordsList.remove(word)
            elif word not in removeSet:
                if word not in self.tagTable.keys():
                    self.tagTable[word] = 0
                self.tagTable[word] = self.tagTable[word] + 1


        #standardizes tagList to be percentages
        wordCount = len(wordsList)
        for word in wordsList:
            word1 = word
            self.tagTable[word] = self.tagTable[word1] / wordCount

    def getTopTags(self, number):
        topTags = dict(sorted(self.tagTable.keys(), key=self.tagTable.__getitem__)[:number])
        return topTags


class tag:
    """Stores all information about a given tag, including lists of which articles
have the tag and the number of times the keywork appears in each."""
    def __init__(self, name):
        self.name = name
        self.taggedArticles = []

    def setArticles(self, articles):
        self.taggedArticles.append(articles)

def articleDistance(art1, art2):
    """returns the pairwise distance between two artilces, calculated from the tags"""
    tags1 = list(art1.tagTable.keys())
    tags2 = list(art2.tagTable.keys())
    tags = tags2.append(tags2)

    distance = 0

    for tag in tags:
        value1 = 0
        value2 = 0
        if tag in tags1:
            value1 = art1.tagTable[tag]
        if tag in tags2:
            value2 = art2.tagTable[tag]
        distance = abs(value1 - value2)
        disatnce = distance / len(tags)

    return distance
    

articlesSet = []
for entry in NYTAmericas.entries:
    print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    articlesSet.append(ParsedEntry(toParse.title, toParse.text, entry.link))
    print((articlesSet[len(articlesSet)-1].tagTable))

