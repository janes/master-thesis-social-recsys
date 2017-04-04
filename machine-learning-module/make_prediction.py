import sys, os, math, re, unicodedata, click, requests
from timeit import default_timer as timer
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords
from pymongo import MongoClient
from bson.objectid import ObjectId
from pyspark import SparkConf, SparkContext
from Classifier import Classifier
from twython import Twython
import facebook
from langdetect import detect
#from base import *
# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')
start = timer()
APP_NAME = 'Recomender System'
threshold = 0.02
numMaxSuggestionsPerPost = 5
numStarts = 5
def main(**kwargs):
iduser = sys.argv[1]
#Find user by id
user = findUserById(iduser)
#Find tweets and posts
posts = findPosts(user)
conf = SparkConf().setAppName(APP_NAME)
sc = SparkContext(conf=conf)
postsRDD = sc.parallelize(posts)
tokens, category, categoryAndSubcategory = getTokensAndCategories()
stpwrds = stopwords.words('portuguese')
productRDD = sc.parallelize(findProductsByCategory([]))
productAndPostRDD = productRDD.union(postsRDD)
corpusRDD = (productAndPostRDD.map(lambda s: (s[0], word_tokenize(s[1].lower()), s[2], s[3]))
.map(lambda s: (s[0], [PorterStemmer().stem(x) for x in s[1] if x not in stpwrds], s[2], s[3]))
.map(lambda s: (s[0], [x for x in s[1] if x in tokens], s[2], s[3]))
.filter(lambda x: len(x[1]) >= 20 or x[2] == u'Post')
.cache())
idfsRDD = idfs(corpusRDD)
idfsRDDBroadcast = sc.broadcast(idfsRDD.collectAsMap())
tfidfRDD = corpusRDD.map(lambda x: (x[0], tfidf(x[1], idfsRDDBroadcast.value), x[2], x[3])).cache()
tfidfPostsRDD = tfidfRDD.filter(lambda x: x[2]=='Post').cache()
tfidfPostsBroadcast = sc.broadcast(tfidfPostsRDD.map(lambda x: (x[0], x[1])).collectAsMap())
corpusPostsNormsRDD = tfidfPostsRDD.map(lambda x: (x[0], norm(x[1]))).cache()
corpusPostsNormsBroadcast = sc.broadcast(corpusPostsNormsRDD.collectAsMap())
classifier = Classifier(sc, 'NaiveBayes')
modelNaiveBayesCategory = classifier.getModel('/dados/models/naivebayes/category_new')
postsSpaceVectorRDD = classifier.createVectSpacePost(tfidfPostsRDD, tokens)
predictions = postsSpaceVectorRDD.map(lambda p: (modelNaiveBayesCategory.predict(p[1]),
p[0])).groupByKey().mapValues(list).collect()
for prediction in predictions:
category_to_use = categoryAndSubcategory[int(prediction[0])][0]
tfidfProductsCategoryRDD = tfidfRDD.filter(lambda x: x[2]==category_to_use).cache()
tfidfProductsCategoryBroadcast = sc.broadcast(tfidfProductsCategoryRDD.map(lambda x: (x[0], x[1])).collectAsMap())
corpusInvPairsProductsRDD = tfidfProductsCategoryRDD.flatMap(lambda r: ([(x, r[0]) for x in r[1]])).cache()
corpusInvPairsPostsRDD = tfidfPostsRDD.flatMap(lambda r: ([(x, r[0]) for x in r[1]])).filter(lambda x: x[1] in
prediction[1]).cache()
commonTokens = (corpusInvPairsProductsRDD.join(corpusInvPairsPostsRDD)
.map(lambda x: (x[1], x[0]))
.groupByKey()
.cache())
corpusProductsNormsRDD = tfidfProductsCategoryRDD.map(lambda x: (x[0], norm(x[1]))).cache()
corpusProductsNormsBroadcast = sc.broadcast(corpusProductsNormsRDD.collectAsMap())
similaritiesRDD = (commonTokens
.map(lambda x: cosineSimilarity(x, tfidfProductsCategoryBroadcast.value, tfidfPostsBroadcast.value,
corpusProductsNormsBroadcast.value, corpusPostsNormsBroadcast.value))
.cache())
suggestions = (similaritiesRDD
.map(lambda x: (x[0][1], (x[0][0], x[1])))
.filter(lambda x: x[1][1]>threshold)
.groupByKey()
.mapValues(list)
.join(postsRDD)
.join(postsRDD.map(lambda x: (x[0], x[3])))
.collect())
if len(suggestions) > 0:
insertSuggestions(suggestions, iduser, productRDD)
user['statusRecomendacao'] = u'F'
updateUser(user)
elap = timer()-start
print 'it tooks %d seconds' % elap
if __name__ == '__main__':
main()
