import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.preprocessing import binarize

datasetPath = os.path.join( r"DatasetPrep", r"Dataset" )
cleanTXTPath = os.path.join( datasetPath, r"CleanTXTs" )
articleList = []
labelList = []
genreDict = {
    "Entertainment": 0,
    "Finance": 1,
    "Politics": 2,
    "Sports": 3,
    "Technology": 4,
    "Health": 5
}
featureCount = int( sys.argv[1] )

def prepArticleList():
    with os.scandir( cleanTXTPath ) as Genres:
        for Genre in Genres:
            if( Genre.is_dir() ):
                genrePath = os.path.join( cleanTXTPath, Genre.name )
                with os.scandir( genrePath ) as Articles:
                    for Article in Articles:
                        if( Article.is_file() ):
                            if(  Article.name.endswith( ".txt" )  ):
                                articlePath = os.path.join( genrePath, Article.name )
                                articleList.append( articlePath )
                                labelList.append(  genreDict[ Genre.name ]  )


def prepVectors():
    Vectorizer = TfidfVectorizer( input = 'filename', min_df = 50, ngram_range = (1,2), sublinear_tf=True )
    Vectors = Vectorizer.fit_transform(articleList)

    featureNames = Vectorizer.get_feature_names()
    denseList = Vectors.todense().tolist()
    vectorFrame = pd.DataFrame(denseList, columns = featureNames)

    kBest = SelectKBest( score_func=chi2, k="all" )
    kBestFeatures = kBest.fit( Vectors, labelList )
    scoreFrame = pd.DataFrame( kBestFeatures.scores_ )
    columnFrame = pd.DataFrame( featureNames )
    featureScoreFrame = pd.concat( [columnFrame, scoreFrame], axis=1)
    featureScoreFrame.columns = ["Features", "Score"]
    featureScoreFrame = featureScoreFrame.nlargest( featureCount, "Score" )

    featureNames = set( featureNames )
    topFeatureSet = set( featureScoreFrame["Features"] )
    dropFeatures = featureNames - topFeatureSet
	
    vectorFrame = vectorFrame.drop(  columns = list( dropFeatures )  )
    binarize(X = vectorFrame, copy = False)
    vectorFrame = vectorFrame.astype(int)
    vectorFrame["CATEGORY"] = labelList
    
    finalFeaturePath = os.path.join( datasetPath, "topFeaturesTFIDF.csv" )
    vectorFrame.to_csv( finalFeaturePath, index = False )


def main():
    prepArticleList()
    prepVectors()

if __name__ == "__main__":
    main()
