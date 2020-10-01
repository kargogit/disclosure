"""
    This assumes multiple text files containing individual news stories stored in directories
    pertaining to their content categories
"""
import os
import re
import pandas as pd

datasetPath = os.path.join( "DatasetPrep", "Dataset" )
textPath = os.path.join( datasetPath, "TXTs" )
with os.scandir( textPath ) as Entries:
    for Entry in Entries:
        if( Entry.is_dir() ):
            textDir = os.path.join( textPath, Entry.name )
            JSONFrame = pd.DataFrame()
            with os.scandir( textDir ) as textIter:
                for textEntry in textIter:
                    TXTMatch = re.search(".+\.txt", textEntry.name)
                    if( TXTMatch is not None ):
                        txtFilePath = os.path.join( textDir, textEntry.name )
                        textData = ""
                        with open( file = txtFilePath, mode = "r", encoding = "utf-8", errors = "ignore" ) as textFile:
                            textData = textFile.read()
                        textData = re.sub( '[^a-zA-Z ]+', ' ', textData )
                        JSONFrame = JSONFrame.append(  { "Text": textData },  ignore_index = True  )
            JSONName = Entry.name + ".json"
            JSONPath = re.sub( "TXT", "JSON", textPath )
            resultPath = os.path.join( JSONPath, JSONName )
            JSONFrame.to_json( resultPath )