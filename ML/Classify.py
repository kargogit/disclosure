import os
import re
import pandas as pd
import numpy as np
import json
import spacy
from joblib import load

categoryDict = {
    0: "Entertainment",
    1: "Financial",
    2: "Politics",
    3: "Sports",
    4: "Technology",
    5: "Health",
    6: "Others"
}

classifyDict = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: []
}

showcasePath = os.path.join( r"Showcase" )
datasetPath = os.path.join( showcasePath, r"Dataset" )
JSONPath = os.path.join( datasetPath, r"JSONs" )
cleanTXTPath = os.path.join( datasetPath, r"CleanTXTs" )
modelPath = os.path.join( r"ML", r"Models", r"LogRegClassifier.pkl" )
featureFramePath = os.path.join( datasetPath, r"topFeaturesTFIDF.csv" )

NLP = spacy.load( "en_core_web_lg" )

def getClusters( predictionList ):
    if(  len( predictionList ) == 0  ):
        return []
    
    articleList = []
    resultClusters = []
    
    for trueArticleNum in predictionList:
        cleanArticlePath = os.path.join( cleanTXTPath, str( articleNum ) + ".txt" )
        Article = ""
        with open( file = cleanArticlePath, mode = 'r', errors = "ignore" ) as cleanArticleFile:
			Article = cleanArticleFile.read()
        articleList.append(  NLP( Article )  )

    for articleNum in range(  len( articleList )  ):
		for clusterNum in range(  len( resultClusters )  ):
			clusterSet = resultClusters[ clusterNum ]
			clusterMeanSim = 0
			for articleNumII in clusterSet:
				clusterMeanSim += articleList[ articleNum ].similarity(  articleList[ articleNumII ]  )
			clusterMeanSim /= len( clusterSet )
			if( clusterMeanSim > 0.927 ):
				clusterSet.add( articleNum )
				continue
			
		Cluster = set()
		Cluster.add( articleNum )
		resultClusters.append( Cluster )

    resultClusterList = []

    for clusterSet in resultClusters:
        trueNumCluster = set()
        for articleNum in clusterSet:
            trueNumCluster.add(  predictionList[ articleNum ]  )
        resultClusterList.append( trueNumCluster )
    
    return resultClusterList


def generateFinalJSON( clusterDict ):
    completeActualData = {}
    for Key in clusterDict:
        actualDataOfKey = []
        for Cluster in clusterDict[ Key ]:
            actualDataOfCluster = []
            for articleNum in Cluster:
                filePath = os.path.join(  JSONPath, str( articleNum ) +".json"  )
                JSONData = ""
                with open( file = filePath, mode = 'r', errors = "ignore" ) as txtFile:
                    JSONData = txtFile.read()
                Article = json.loads( JSONData )
                actualDataOfCluster.append( Article )
            actualDataOfKey.append( actualDataOfCluster )
        completeActualData[Key] = actualDataOfKey
    return completeActualData


def main():
    featureList = pd.read_csv(featureFramePath).columns.tolist()[:-1]
    featureLen = len( featureList )
	
    Classifier = load(modelPath)
    
    with os.scandir( JSONPath ) as Entries:
        for Entry in Entries:
            if( Entry.is_file() ):
                JSONMatch = re.search( ".+\.json", Entry.name )
                if( JSONMatch is not None ):
                    fileCounter = 0
                    
                    filePath = os.path.join( JSONPath, Entry.name )
                    articleName = Entry.name[:-5]
                    outPath = os.path.join( cleanTXTPath, articleName )
                    
                    Article = ""
                    with open( file = filePath, mode = 'r', errors = "ignore" ) as txtFile:
						Article = txtFile.read()
                    Article = json.loads( Article )
                    Article = Article["Text"]

                    Article = Article.lower()
                    Article = re.sub( "[^a-z ]+", " ", Article )
                    Article = re.sub( "  +", " ", Article )
                    Article = NLP(Article)
                    tempArticle = [ Word.lemma_ for Word in Article if not Word.is_stop ]
                    Article = " ".join( tempArticle )
                        
                    occurList = [  int( Feature in Article ) for Feature in featureList  ]
                    occurFrame = np.asarray( occurList, dtype = int ).reshape(1, -1)
                    Prediction = Classifier.predict( occurFrame )
                    maxDecisionFn = max(  Classifier.decision_function( occurFrame )[0]  )
                        
                    if( maxDecisionFn >= 0.0 ):
                        classifyDict[Prediction].append(  int( articleName )  )
                    else:
                        classifyDict[6].append(  int( articleName )  )
                        
                    outFilePath = os.path.join( outPath, articleName + ".txt" )
                    with open( file = outFilePath ) as newFile:
                        newFile.write( Article )
						
	clusterDict = {}
	for Key in classifyDict.keys():
		clusterDict[  categoryDict[ Key ]  ] = getClusters(  classifyDict[ Key ]  )
    
    finalFile = generateFinalJSON( clusterDict )
    finalFilePath = os.path.join( showcasePath, r"ShowcaseDataset.jsonp" )
    with open( finalFilePath, 'w' ) as finalFilePointer:
        json.dump( finalFile, finalFilePointer )

	JSONData = ""
    with open( file = finalFilePath, mode="r", encoding="utf-8", errors="ignore" ) as txtFile:
        JSONData = txtFile.read()
    JSONData = r"MyData = [" + JSONData + r"]"

    with open( file = finalFilePath, mode="w", encoding="utf-8" ) as txtFile:
        txtFile.write(JSONData)


if __name__ == "__main__":
    main()
