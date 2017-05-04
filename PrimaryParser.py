from nltk.corpus import stopwords
from newspaper import Article
import feedparser
from collections import Counter
import numpy
from sklearn.cluster import KMeans
from sklearn import metrics
#import matplotlib.pyplot as plt

NYTAmericas = feedparser.parse("http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml")
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

def tagDistanceMatrix(tagSet, labels, articleSet):
    """builds binary array filled with which articles have what tags"""
    #for article in articleSet:
    #    for tag in tagSet:
    #        print(article in tagSet[tag])
    distances = numpy.array([[(article in tagSet[tag]) for article in articleSet] 
          for tag in labels])
    return distances        
    

   
articleSet = []
tagSet = {} #keys are tag names, value is list of articles with that tag
i = 0

for entry in NYTAmericas.entries:
    #print(entry.link)
    toParse = Article(entry.link)
    toParse.download()
    toParse.parse()
    entry = ParsedEntry(toParse.title, toParse.text, entry.link)
    articleSet.append(entry)
    #print(articleSet[i].tagTable)
    topTags = articleSet[i].getTopTags(30)
    #print(topTags)
    initTags(topTags, tagSet, entry)
    i+=1

tagFlag = True
print("Clustering tags, not articles: ", tagFlag)
print("Articles: " + i.__str__())
labels = tagSet.keys() #want to ENSURE the ordering is the same now and later
print("Labels: " + len(labels).__str__())
print("Beginning K means now with k=1:")
distances = tagDistanceMatrix(tagSet, labels, articleSet)
if tagFlag is False:
    distances = numpy.transpose(distances)
km = KMeans(n_clusters = 1, random_state = 0).fit(distances)
initInertia = km.inertia_
print(initInertia)
elbowed = False
k = 1
while not elbowed and k < len(articleSet)-1:
    k+=1
    print("k = " + k.__str__())
    km = KMeans(n_clusters = k, random_state = 0).fit(distances)
    newInertia = km.inertia_
    print(newInertia)
    if newInertia > (initInertia * .95):
        elbowed = True
    else:
        initInertia = newInertia


print(km.labels_)
labels = list(labels)
if tagFlag is False: #make labels article names, not tags
    labels = [article.title for article in articleSet]
clusters = [[] for i in range (0, k)]
for i in range(0, len(km.labels_)):
    clusters[km.labels_.item(i)].append(labels[i])
for i in range (0, k):
    print("Cluster ", i, " is: ", clusters[i])
