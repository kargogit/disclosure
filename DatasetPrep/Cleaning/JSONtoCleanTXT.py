import os
import re
import pandas as pd
import json
import spacy
import en_core_web_lg

datasetPath = os.path.join( r"DatasetPrep", r"Dataset" )
JSONPath = os.path.join( datasetPath, r"JSONs" )
cleanTXTPath = os.path.join( datasetPath, r"CleanTXTs" )
NLP = en_core_web_lg.load()
with os.scandir( JSONPath ) as Entries:
    for Entry in Entries:
        if( Entry.is_file() ):
            JSONMatch = re.search( ".+\.json", Entry.name )
            if( JSONMatch is not None ):
                fileCounter = 0
                filePath = os.path.join( JSONPath, Entry.name )
                Articles = pd.DataFrame(
                    json.load(
                        open( file = filePath, mode = 'r', encoding = "utf-8", errors = "ignore" )
                    )
                )
                outPath = os.path.join( cleanTXTPath, Entry.name[:-5] )
                Articles = Articles["Content"].tolist()
                for Article in Articles:
                    Article = Article.lower()
                    Article = re.sub( "[^a-z ]+", " ", Article )
                    Article = re.sub( "  +", " ", Article )
                    Article = NLP(Article)
                    tempArticle = [ Word.lemma_ for Word in Article if not Word.is_stop ]
                    Article = " ".join( tempArticle )
                    outFilePath = os.path.join(  outPath, str( fileCounter ) + ".txt"  )
                    newFile = open( outFilePath, "w" )
                    newFile.write( Article )
                    newFile.close()
                    fileCounter += 1
