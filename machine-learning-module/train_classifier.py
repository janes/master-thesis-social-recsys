import sys, os, math, datetime
from timeit import default_timer as timer
import re, unicodedata
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords
from pymongo import MongoClient
from pyspark import SparkConf, SparkContext
from Classifier import Classifier
from base import *
APP_NAME = 'Recomender System - Spark Job'
def main(sc):
stpwrds = stopwords.words('portuguese')
products = findProductsByCategory([])
productRDD = sc.parallelize(products)
corpusRDD = productRDD.map(lambda s: (s[0], word_tokenize(s[1].lower()), s[2], s[3])).map(lambda s: (s[0],
[PorterStemmer().stem(x) for x in s[1] if x not in stpwrds], s[2], s[3] )).map(lambda s: (s[0], [x[0] for x in pos_tag(s[1]) if x[1] ==
'NN' or x[1] == 'NNP'], s[2], s[3])).cache()
idfsRDD = idfs(corpusRDD)
idfsRDDBroadcast = sc.broadcast(idfsRDD.collectAsMap())
tfidfRDD = corpusRDD.map(lambda x: (x[0], tfidf(x[1], idfsRDDBroadcast.value), x[2], x[3]))
category = productRDD.map(lambda x: x[2]).distinct().collect()
categoryAndSubcategory = productRDD.map(lambda x: (x[2], x[3])).distinct().collect()
tokens = corpusRDD.flatMap(lambda x: x[1]).distinct().collect()
insertTokensAndCategories(tokens, category, categoryAndSubcategory)
# INIT
classifier = Classifier(sc, 'NaiveBayes')
classifierDT = Classifier(sc, 'DecisionTree')
trainingVectSpaceCategoryRDD, testVectSpaceCategoryRDD = classifier.createVectSpaceCategory(tfidfRDD, category,
tokens).randomSplit([8, 2], seed=0L)
trainingVectSpaceSubcategory, testVectSpaceSubcategory = classifier.createVectSpaceSubcategory(tfidfRDD,
categoryAndSubcategory, tokens).randomSplit([8, 2], seed=0L)
trainingVectSpaceCategoryRDD, testVectSpaceCategoryRDD = classifierDT.createVectSpaceCategory(tfidfRDD, category,
tokens).randomSplit([8, 2], seed=0L)
trainingVectSpaceSubcategoryRDD, testVectSpaceSubcategoryRDD = classifierDT.createVectSpaceSubcategory(tfidfRDD,
categoryAndSubcategory, tokens).randomSplit([8, 2], seed=0L)
# NB CAT
modelNaiveBayesCategory = classifier.trainModel(trainingVectSpaceCategoryRDD,'/dados/models/naivebayes/category_new')
nbcat_start = timer()
predictionAndLabelCategoryRDD = testVectSpaceCategoryRDD.map(lambda p :
(category[int(modelNaiveBayesCategory.predict(p.features))], category[int(p.label)]))
acuraccyCategory = float(predictionAndLabelCategoryRDD.filter(lambda (x, v): x[0] ==
v[0]).count())/float(predictionAndLabelCategoryRDD.count())
print 'the accuracy of the Category Naive Bayes model is %f' % acuraccyCategory
elapnbcat = timer()-nbcat_start
print 'NB CAT tooks %d seconds' % elapnbcat
# NB SUBCAT
modelNaiveBayesSubcategory = classifier.trainModel(trainingVectSpaceSubcategory,
'/dados/models/naivebayes/subcategory_new')
nbsubcat_start = timer()
predictionAndLabelSubcategory = testVectSpaceSubcategory.map(lambda p :
(categoryAndSubcategory[int(modelNaiveBayesSubcategory.predict(p.features))], categoryAndSubcategory[int(p.label)]))
acuraccySubcategory = float(predictionAndLabelSubcategory.filter(lambda (x, v): x[0] ==
v[0]).count())/float(predictionAndLabelSubcategory.count())
print 'the accuracy of the Subcategory Naive Bayes model is %f' % acuraccySubcategory
elapnbsubcat = timer()-nbsubcat_start
print 'NB SUBCAT tooks %d seconds' % elapnbsubcat
#DT CAT
modelDecisionTreeCategory = classifierDT.trainModel(trainingVectSpaceCategory, '/dados/models/dt/category_new')
dtcat_start = timer()
predictions = modelDecisionTreeCategory.predict(testVectSpaceCategory.map(lambda x: x.features))
predictionAndLabelCategory = testVectSpaceCategory.map(lambda lp: lp.label).zip(predictions)
acuraccyDecisionTree = float(predictionAndLabelCategory.filter(lambda (x, v): x ==
v).count())/float(predictionAndLabelCategory.count())
print 'the accuracy of the Decision Tree model is %f' % acuraccyDecisionTree
elapdtcat = timer()-dtcat_start
print 'DT CAT tooks %d seconds' % elapdtcat
#DT SUBCAT
modelDecisionTreeSubcategory = classifierDT.trainModel(trainingVectSpaceSubcategory,
'/dados/models/dt/subcategory_new')
dtsubcat_start = timer()
predictions = modelDecisionTreeSubcategory.predict(testVectSpaceSubcategory.map(lambda x: x.features))
predictionAndLabelSubcategory = testVectSpaceSubcategory.map(lambda lp: lp.label).zip(predictions)
acuraccyDecisionTree = float(predictionAndLabelSubcategory.filter(lambda (x, v): x ==
v).count())/float(predictionAndLabelSubcategory.count())
print 'the accuracy of the Decision Tree model is %f' % acuraccyDecisionTree
elapdtsubcat = timer()-dtsubcat_start
print 'DT SUB CAT tooks %d seconds' % elapdtsubcat
if __name__ == '__main__':
conf = (SparkConf().setAppName("RECSYS"))
sc = SparkContext(conf=conf)
main(sc)