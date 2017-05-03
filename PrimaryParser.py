from nltk.corpus import stopwords
from newspaper import Article
import feedparser
from collections import Counter

NYTAmericas = feedparser.parse("http://www.nytimes.com/services/xml/rss/nyt/Americas.xml")
removeSet = set(stopwords.words('english'))
removeSet.update(['lately', 'wanted', 'call', 'later', 'latest', 'main', 'said','way', 'many', 'available', 'efforts', 'similar', 'programadvertisement', 'multiple', 'months' 'essentially', 'identify', 'include', 'name'])
class ParsedEntry:
    #Not called article to avoid conflict with Newspaper package
    def __init__(self, name, body, link):
        
        self.url = link
        self.title = name
        self.tagTable, self.cleanWordsList = self._preprocessText(body)

    def _preprocessText(self, body):
        tagTable = {}
        #sanitizes text, sets everything to lowercase, removes numbers and symbols but keeps spaces leading to just words separated by spaces.
        lowercaseText = body.lower()
        newStr = ""
        for c in lowercaseText:
            if c.isalpha() or c==" ":
                newStr+=c
        self.text = newStr

        #creates dictionary with word occurances in the occurrenceTable dictionary object.
        wordsList = self.text.split()
        cleanWordsList = []
        for word in wordsList:
            if word not in removeSet:
                if word not in tagTable.keys():
                    tagTable[word] = 0
                tagTable[word] = tagTable[word] + 1
                cleanWordsList.append(word)

        return tagTable, cleanWordsList


    def getTopTags(self, number):
        #http://stackoverflow.com/questions/11902665/top-values-from-dictionary
        top = Counter(self.tagTable)
        top.most_common()
        topTags = {}
        for k, v in top.most_common(10):
            topTags[k] = v
        return topTags

def articleDistance(art1, art2):
    """returns the pairwise distance between two artilces, calculated from the tags"""
    tags1 = list(art1.tagTable.keys())
    tags2 = list(art2.tagTable.keys())
    tags = tags1[:]
    tags.append(tags2)

    distance = 0

    for tag in tags:
        value1 = 0
        value2 = 0
        if tag in tags1:
            value1 = art1.tagTable[tag]
        if tag in tags2:
            value2 = art2.tagTable[tag]
        distance = distance + abs(value1 - value2)
        distance = distance / len(tags)

    return distance
    
def initTags(topTags, tagSet, article):
    for tag in topTags:
        if tag in tagSet.keys():
            tagSet[tag].append(article)
        else:
            tagSet[tag] = [article]

def tagDistanceMatrix(tagSet, articleSet):
    """builds binary array filled with which articles have what tags"""
    distances = numpy.array([[(article in tagSet[tag]) for article in articleSet] 
          for tag in tagSet.keys()])
    return distances        
    

   
articleSet = []
tagSet = {} #keys are tag names, value is list of articles with that tag
i = 0
for entry in NYTAmericas.entries:
    print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    articleSet.append(ParsedEntry(toParse.title, toParse.text, entry.link))
    print(articleSet[i].tagTable)
    topTags = articleSet[i].getTopTags(10)
    print(topTags)
    initTags(topTags, tagSet, toParse.title)
    i+=1

print(articleDistance(articleSet[0], articleSet[1]))
