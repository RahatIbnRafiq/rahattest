from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets
import nolearnOld
from nolearnOld import dbn
from sklearn.linear_model import Perceptron
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from csv import DictReader
from collections import defaultdict
from numpy import array
from sklearn.metrics import precision_recall_fscore_support

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.svm import SVC
from sklearn.datasets import load_digits


import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
from sklearn.feature_selection import RFE
from sklearn.svm import LinearSVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score

import databaseCodes.mongoOperations as mongoOperations
from collections import defaultdict
import re
from sklearn import linear_model


from textblob import TextBlob
import nltk
from nltk import bigrams
from nltk import trigrams
from lasagne.layers.noise import dropout
import math


negWordList = []


def populateNegWord():
    
    total_data = open("swearWords.csv", 'r')
    
    for line in total_data:
        words = line.split(",")
        for word in words:
            negWordList.append(word)
    
    print negWordList
    
    
def getBiGramsFromComments(text):
    # split the texts into tokens
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
    bi_tokens = bigrams(tokens)
    fdist = nltk.FreqDist(bi_tokens)
    return fdist

def getTriGramsFromComments(text):
    # split the texts into tokens
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
    tri_tokens = trigrams(tokens)
    fdist = nltk.FreqDist(tri_tokens)
    return fdist

def getUnigramsFromComments(text):
    tokens = nltk.word_tokenize(text)
    return tokens

def loadEmotionDictionary():
    total_data = DictReader(open("video_categorization.csv", 'Ur'))
    emotionDictionary = defaultdict(str)
    for data in total_data:
        emotion = str(data["question2"])
        videolink = str(data["videolink"])
        emotionDictionary[videolink] = emotion
    return emotionDictionary

def loadContentDictionary():
    total_data = DictReader(open("video_categorization.csv", 'Ur'))
    emotionDictionary = defaultdict(str)
    for data in total_data:
        emotion = str(data["question3"])
        videolink = str(data["videolink"])
        emotionDictionary[videolink] = emotion
    return emotionDictionary




def FeatureExtractionVersionTwo(data,emotionDictionary,contentdictionary):
    featureDictionary = defaultdict(int)
    
    videolink = data["videolink"]
    emotion = str(emotionDictionary[videolink])
    content = str(contentdictionary[videolink])
    
    #user features
    featureDictionary["userFollowerCount"] = int(data["userFollowerCount"])
    featureDictionary["userFollowingCount"] = int(data["userFollowingCount"])
    featureDictionary["userloopCount"] = int(data["userloopCount"])
    featureDictionary["userAuthoredPostCountCount"] = int(data["userAuthoredPostCountCount"])
    featureDictionary["userLikeCount"] = int(data["userLikeCount"])
    featureDictionary["userPostCount"] = int(data["userPostCount"])
    featureDictionary["userDescriptionPolarity"] =float(1.0- float(data["userDescriptionPolarity"]))
    featureDictionary["userDescriptionSubjectivity"] = float(1.0- float(data["userDescriptionSubjectivity"]))
    
    
    #media session features
    
    
    featureDictionary["postLikeCount"] = int(data["postLikeCount"])
    featureDictionary["postLoopCount"] = int(data["postLoopCount"])
    featureDictionary["postCommentCount"] = int(data["postCommentCount"])
    featureDictionary["postRepostCount"] = int(data["postRepostCount"])
    featureDictionary["postExplicitContent"] = int(data["postExplicitContent"])
    featureDictionary["postDescriptionPolarity"] = float(1.0- float(data["postDescriptionPolarity"]))
    featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(data["postDescriptionSubjectivity"]))
        
    #comment features
    
    featureDictionary["tagCount"] = int(data["tagCount"])
    featureDictionary["mentionCount"] = int(data["mentionCount"])
    featureDictionary["otherCount"] = int(data["otherCount"])
    featureDictionary["verifiedCount"] = int(data["verifiedCount"])
    featureDictionary["nonVerifiedCount"] = int(data["nonVerifiedCount"])
    
    featureDictionary["ownerCommentCount"] = int(data["ownerCommentCount"])
    featureDictionary["ownerCommentPolarityTotal"] = 100.0 + float(data["ownerCommentPolarityTotal"])
    featureDictionary["ownerCommentSubjectivityTotal"] = 100.0 + float(data["ownerCommentSubjectivityTotal"])
    
    
    featureDictionary["otherCommentCount"] = int(data["otherCommentCount"])
    featureDictionary["otherCommentPolarityTotal"] = float(100.0 + float(data["otherCommentPolarityTotal"]))
    featureDictionary["otherCommentSubjectivityTotal"] = float(100.0 + float(data["otherCommentSubjectivityTotal"]))
    
    featureDictionary["allCommentPolarityTotal"] = float(100.0 + float(data["allCommentPolarityTotal"]))
    featureDictionary["allCommentSubjectivityTotal"] = float(100.0 + float(data["allCommentSubjectivityTotal"]))
    
    featureDictionary["negativeCommentCount"] = int(float(data["negativeCommentCount"]))
    featureDictionary["negativeWordCount"] = int(data["negativeWordCount"])
    featureDictionary["negativePolarityTotal"] = float(100.0 + float(data["negativePolarityTotal"]))
    featureDictionary["negativeSubjectivityTotal"] = float(100.0 +float(data["negativeSubjectivityTotal"]))
    featureDictionary["negativeCommentPercentage"] = float(data["negativeCommentPercentage"])
    featureDictionary["negativeWordPerNegativeComment"] = float(data["negativeWordPerNegativeComment"])
    

    featureDictionary[emotion]+=1
    featureDictionary[content]+=1
           

    return featureDictionary
    

def featureSelectionProcess(X,Y,featureSelection):
    print "feature selection process: "+str(featureSelection)
    print "before feature selection. shape of X"+str(X[0].shape)
    if featureSelection == "linearSVM":
        X_new = LinearSVC(C=0.01, penalty="l1", dual=False).fit_transform(X, Y)
        print  "after feature selection. shape of X"+str(X_new[0].shape)
    elif featureSelection == "SelectKBest":
        X_new = SelectKBest(chi2, k=6).fit_transform(X, Y)
        print  "after feature selection. shape of X"+str(X_new[0].shape)
    elif featureSelection == "SelectKPercentile":
        selector = SelectPercentile(f_classif, percentile=30)
        X_new = selector.fit_transform(X, Y)
        print  "after feature selection. shape of X"+str(X_new[0].shape)
    elif featureSelection == "TreeBased":
        clf = ExtraTreesClassifier()
        X_new = clf.fit(X, Y).transform(X)
        print  "after feature selection. shape of X"+str(X_new[0].shape)
    elif featureSelection == "Recursive":
        svc = SVC(kernel="linear", C=1)
        rfe = RFE(estimator=svc, n_features_to_select=5, step=1)
        X_new = rfe.fit(X, Y).transform(X)
        print  "after feature selection. shape of X"+str(X_new[0].shape)


def SplitIntoTestTrainingDataset(filename,emotionDictionary,contentdictionary):
    total_data = DictReader(open(filename, 'Ur'))
    bullyingCount = 0
    notBullyngCount = 0
    
    trainingData = []
    trainingLabel = []
    testData = []
    testLabel = []
    count = 0
    for ii in total_data:
        print count
        count = count + 1
        if float(ii["question2:confidence"]) < 0.6:
            continue
        else:
            if ii["question2"] == "noneBll":
                label = 0
                notBullyngCount = notBullyngCount + 1
                if notBullyngCount > 258: #258
                    continue
                if notBullyngCount > 100:   #100
                    featureDictionary = FeatureExtractionVersionTwo(ii,emotionDictionary,contentdictionary)
                    testData.append(featureDictionary)
                    testLabel.append(label)
                else:
                    featureDictionary = FeatureExtractionVersionTwo(ii,emotionDictionary,contentdictionary)
                    trainingData.append(featureDictionary)
                    trainingLabel.append(label)

            else:
                label = 1
                bullyingCount = bullyingCount + 1
                if bullyingCount > 179:   #179
                    continue
                if bullyingCount > 100:  #100
                    featureDictionary = FeatureExtractionVersionTwo(ii,emotionDictionary,contentdictionary)
                    testData.append(featureDictionary)
                    testLabel.append(label)
                else:
                    featureDictionary = FeatureExtractionVersionTwo(ii,emotionDictionary,contentdictionary)
                    trainingData.append(featureDictionary)
                    trainingLabel.append(label)
            if bullyingCount > 179 and notBullyngCount > 258:
                break
    print str(len(testData))+" test data size"
    print str(len(testLabel))+" test label size"
    
    print str(len(trainingData))+" training data size"
    print str(len(trainingLabel))+" training label size"
    
    totalData = []
    totalLabel = []
    
    for label in trainingLabel:
        totalLabel.append(label)
    for label in testLabel:
        totalLabel.append(label)
    
    for data in trainingData:
        totalData.append(data)
    for data in testData:
        totalData.append(data)
        
    print "total data collected "+str(len(totalLabel))
    print "total label collected "+str(len(totalData))
    

    return(totalData,totalLabel,199)


def TransformIntoVectors(totalData,totalLabel):
    v = DictVectorizer(sparse=True)
    
    X =  v.fit_transform(totalData)   
    Y = array(totalLabel)
    
    return (X,Y)
    

def confidenceLogRegression(theta, X,intercept):
    h = X.dot(theta.T)+intercept
    m = h.size-1
    return h[m] 
    
        
def TransformIntoMatrix(data,target):
    row = data.shape[0]
    column = data.shape[1]
    m = np.empty((row, column))

    for i in range(row):
        k = 0
        for j in data[i].indices:
            m[i][j] = data[i].data[k]
            k = k+1
            
    # Prepend the column of 1s for bias
    N, M  = m.shape
    all_X = np.ones((N, M + 1))
    all_X[:, 1:] = m
    
    return (all_X, target)
    

emotionDictionary = loadEmotionDictionary()
contentdictionary =  loadContentDictionary()

populateNegWord()

print "=========================================================="
totalData,totalLabel,index = SplitIntoTestTrainingDataset("vine_meta_data.csv",emotionDictionary,contentdictionary)
print "getting data is finished successfully"
print "=========================================================="





print "=========================================================="
print "now transforming data into vectorized form"
X,Y = TransformIntoVectors(totalData,totalLabel)
print "data has been convereted into vectorized form successfully"
print "=========================================================="


X_Matrix,Y_Matrix = TransformIntoMatrix(X,Y)
X_Matrix = X_Matrix / X_Matrix.max(axis=0)

X_training_Matrix = X_Matrix[0:200]
Y_training_Matrix = Y_Matrix[0:200]
X_test_Matrix = X_Matrix[200:437]
Y_test_Matrix = Y_Matrix[200:437]

##################### THIS IS LOGISTIC REGRESSION ####################################### 

"""
########################logistic regression with user features###########################################
userFeatureTraining =  X_training_Matrix[0:200,0:8]
userFeatureTest = X_test_Matrix[0:237,0:8]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(userFeatureTraining, Y_training_Matrix)
userFeatureLogRegPreds = logReg.predict(userFeatureTest)
print "logistic regression using user features"
print classification_report(Y_test_Matrix,userFeatureLogRegPreds)
#########################################################################################################




########################logistic regression with media features###########################################
mediaFeatureTraining =  X_training_Matrix[0:200,8:15]
mediaFeatureTest = X_test_Matrix[0:237,8:15]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(mediaFeatureTraining, Y_training_Matrix)
mediaFeatureLogRegPreds = logReg.predict(mediaFeatureTest)
print "logistic regression using media session features"
print classification_report(Y_test_Matrix,mediaFeatureLogRegPreds)
#########################################################################################################




########################logistic regression with comment features###########################################
commentFeatureTraining =  X_training_Matrix[0:200,15:35]
commentFeatureTest = X_test_Matrix[0:237,15:35]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(commentFeatureTraining, Y_training_Matrix)
commentFeatureLogRegPreds = logReg.predict(commentFeatureTest)
print "logistic regression using comment features"
print classification_report(Y_test_Matrix,commentFeatureLogRegPreds)
#########################################################################################################


########################logistic regression with video features###########################################
videoFeatureTraining =  X_training_Matrix[0:200,35:]
videoFeatureTest = X_test_Matrix[0:237,35:]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(videoFeatureTraining, Y_training_Matrix)
videoFeatureLogRegPreds = logReg.predict(videoFeatureTest)
print "logistic regression using video features"
print classification_report(Y_test_Matrix,videoFeatureLogRegPreds)
#########################################################################################################


########################logistic regression with all features###########################################
allFeatureTraining =  X_training_Matrix[0:200,8:35]
allFeatureTest = X_test_Matrix[0:237,8:35]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(allFeatureTraining, Y_training_Matrix)
allFeatureLogRegPreds = logReg.predict(allFeatureTest)
print "logistic regression using all features"
print classification_report(Y_test_Matrix,allFeatureLogRegPreds)
#########################################################################################################
##################### THIS IS LOGISTIC REGRESSION #######################################


"""

##################### THIS IS NEURAL NETWORK #######################################



########################neural network with user features###########################################
"""userFeatureTraining =  X_training_Matrix
userFeatureTest = X_test_Matrix

net1 = NeuralNet(
        layers=[('input', layers.InputLayer),
                ('hidden1', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
        # layer parameters:
        input_shape=userFeatureTraining.shape,
        hidden1_num_units=1000,  # number of units in 'hidden' layer
        output_nonlinearity=lasagne.nonlinearities.softmax,
        output_num_units=2,  

        # optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.1,
        update_momentum=0.9,
        max_epochs=100,
        verbose=1,
        )

net1.fit(userFeatureTraining, Y_training_Matrix)
userFeaturenet1Preds,userFeaturenet1Probs = net1.predict(userFeatureTest)
print "neural network using user features"
print classification_report(Y_test_Matrix,userFeaturenet1Preds)
f = open("NeuralAllNotBullyingThreshold.txt","w")
threshold = 0.0
while threshold < 1:
    i = 0
    correct = 0.0
    total = 0.0
    for x_test in X_test_Matrix:
        truth = Y_test_Matrix[i]
        x_test = np.reshape(x_test, (1, x_test.shape[0])) #reshaping the array into 2D
        x_test = x_test#taking user features
        prediction,confidences = net1.predict(x_test)
        if confidences[0][0] >=threshold:
            prediction = 0
            total = total+1
            if prediction == truth:
                correct = correct + 1
        i = i+1
    try:
        print str(float(correct/total))+","+str(threshold)
        print str(total)+","+str(correct)
        f.write(str(float(correct/total))+","+str(threshold)+"\n")
        print "____________________"
    except Exception as e :
        print "Exception :"+str(e)
        break
    threshold = threshold + 0.01

f.close()
"""

#########################################################################################################


"""
########################neural network with media features###########################################
mediaFeatureTraining =  X_training_Matrix[0:200,8:15]
mediaFeatureTest = X_test_Matrix[0:237,8:15]

net1 = NeuralNet(
        layers=[('input', layers.InputLayer),
                ('hidden1', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
        # layer parameters:
        input_shape=mediaFeatureTraining.shape,
        hidden1_num_units=100,  # number of units in 'hidden' layer
        output_nonlinearity=lasagne.nonlinearities.softmax,
        output_num_units=2,  

        # optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.1,
        update_momentum=0.9,
        max_epochs=100,
        verbose=1,
        )

net1.fit(mediaFeatureTraining, Y_training_Matrix)
mediaFeaturenet1Preds,mediaFeaturenet1Probs = net1.predict(mediaFeatureTest)
print "neural network using media features"
print classification_report(Y_test_Matrix,mediaFeaturenet1Preds)
#########################################################################################################
"""


"""
########################neural network with comment features###########################################
commentFeatureTraining =  X_training_Matrix[0:200,15:35]
commentFeatureTest = X_test_Matrix[0:237,15:35]

net1 = NeuralNet(
        layers=[('input', layers.InputLayer),
                ('hidden1', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
        # layer parameters:
        input_shape=commentFeatureTraining.shape,
        hidden1_num_units=100,  # number of units in 'hidden' layer
        output_nonlinearity=lasagne.nonlinearities.softmax,
        output_num_units=2,  

        # optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.1,
        update_momentum=0.9,
        max_epochs=100,
        verbose=1,
        )

net1.fit(commentFeatureTraining, Y_training_Matrix)
commentFeaturenet1Preds,commentFeaturenet1Probs = net1.predict(commentFeatureTest)
print "neural network using comment features"
print classification_report(Y_test_Matrix,commentFeaturenet1Preds)
#########################################################################################################
"""
"""
########################neural network with video features###########################################
videoFeatureTraining =  X_training_Matrix
videoFeatureTest = X_test_Matrix

net1 = NeuralNet(
        layers=[('input', layers.InputLayer),
                ('hidden1', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
        # layer parameters:
        input_shape=videoFeatureTraining.shape,
        hidden1_num_units=100,  # number of units in 'hidden' layer
        output_nonlinearity=lasagne.nonlinearities.softmax,
        output_num_units=2,  

        # optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.1,
        update_momentum=0.9,
        max_epochs=100,
        verbose=1,
        )

net1.fit(videoFeatureTraining, Y_training_Matrix)
videoFeaturenet1Preds,videoFeaturenet1Probs = net1.predict(videoFeatureTest)
print "neural network using video features"
print classification_report(Y_test_Matrix,videoFeaturenet1Preds)
#########################################################################################################
##################### THIS IS NEURAL NETWORK #######################################
"""



##################### THIS IS DEEP BELIEF NETWORK #######################################
"""
########################deep belief network with video features###########################################
videoFeatureTraining =  X_training_Matrix[0:200,35:]
videoFeatureTest = X_test_Matrix[0:237,35:]
dbn = dbn.DBN(
    [videoFeatureTraining.shape[1],1000,2],
    learn_rates = 0.3,
    learn_rate_decays = 0.9,
    epochs = 10,
    verbose = 1)
dbn.fit(videoFeatureTraining, Y_training_Matrix)
videoFeatureDBNPreds,videoFeatureDBNProbs = dbn.predict(videoFeatureTest)
print classification_report(Y_test_Matrix,videoFeatureDBNPreds)
########################deep belief network with video features###########################################
"""
"""
########################deep belief network with user features###########################################
userFeatureTraining =  X_training_Matrix[0:200,0:8]
userFeatureTest = X_test_Matrix[0:237,0:8]
dbn = dbn.DBN(
    [userFeatureTraining.shape[1],1000,2],
    learn_rates = 0.3,
    learn_rate_decays = 0.9,
    epochs = 10,
    verbose = 1)
dbn.fit(userFeatureTraining, Y_training_Matrix)
userFeatureDBNPreds,userFeatureDBNProbs = dbn.predict(userFeatureTest)
print classification_report(Y_test_Matrix,userFeatureDBNPreds)
########################deep belief network with user features###########################################
"""
"""
########################deep belief network with media features###########################################
mediaFeatureTraining =  X_training_Matrix[0:200,8:15]
mediaFeatureTest = X_test_Matrix[0:237,8:15]
dbn = dbn.DBN(
    [mediaFeatureTraining.shape[1],1000,2],
    learn_rates = 0.3,
    learn_rate_decays = 0.9,
    epochs = 10,
    verbose = 1)
dbn.fit(mediaFeatureTraining, Y_training_Matrix)
mediaFeatureDBNPreds,mediaFeatureDBNProbs = dbn.predict(mediaFeatureTest)
print classification_report(Y_test_Matrix,mediaFeatureDBNPreds)
########################deep belief network with media features###########################################
"""

########################deep belief network with comment features###########################################
commentFeatureTraining =  X_training_Matrix[0:200,15:35]
commentFeatureTest = X_test_Matrix[0:237,15:35]
dbn = dbn.DBN(
    [commentFeatureTraining.shape[1],1000,2],
    learn_rates = 0.1,
    learn_rate_decays = 0.9,
    epochs = 100,
    verbose = 1)
dbn.fit(commentFeatureTraining, Y_training_Matrix)
commentFeatureDBNPreds,commentFeatureDBNProbs = dbn.predict(commentFeatureTest)
print classification_report(Y_test_Matrix,commentFeatureDBNPreds)
########################deep belief network with media features###########################################

##################### THIS IS BELIEF NETWORK ############################################


"""userFeatureTraining =  X_training_Matrix[0:200,35:]
logReg = linear_model.LogisticRegression(C=1e6)
logReg.fit(userFeatureTraining, Y_training_Matrix)


print str(X_test_Matrix.shape)+" shape of test matrix"
print "logistic regression using user features"


f = open("logRegVideoBullyingThreshold.txt","w")
threshold = 0.0
while threshold < 5:
    i = 0
    correct = 0.0
    total = 0.0
    for x_test in X_test_Matrix:
        x_test = np.reshape(x_test, (1, x_test.shape[0])) #reshaping the array into 2D
        x_test = x_test[:,35:]#taking user features
        prediction = logReg.predict(x_test)[0]
        truth = Y_test_Matrix[i]
        theta = logReg.coef_[0]
        intercept =  logReg.intercept_
        confidence = abs(confidenceLogRegression(theta, x_test,intercept)-0)
        if confidence >=threshold:
            if prediction == 1:
                total = total+1
                if prediction == truth:
                    correct = correct + 1
        i = i+1
    try:
        print str(float(correct/total))+","+str(threshold)
        print str(total)+","+str(correct)
        f.write(str(float(correct/total))+","+str(threshold)+"\n")
        print "____________________"
    except Exception:
        print "Exception"
        break
    threshold = threshold + 0.1

f.close()
"""
print "done"

