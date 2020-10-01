import os
import re
import pandas as pd

datasetPath = os.path.join( "DatasetPrep", "Dataset" )
CSVPath = os.path.join( datasetPath, "CSVs" )
with os.scandir( CSVPath ) as Entries:
    for Entry in Entries:
        if( Entry.is_file() ):
            CSVMatch = re.search(".+\.csv", Entry.name)
            if( CSVMatch is not None ):
                filePath = os.path.join( CSVPath, Entry.name )
                CSVData = pd.read_csv( filePath )
                CSVData = pd.DataFrame( CSVData["Content"] )
                CSVData = CSVData.rename( columns = { "Content": "Text" } )
                JSONPath = re.sub( "CSV", "JSON", CSVPath )
                resultPath = os.path.join(  JSONPath, re.sub( "csv", "json", Entry.name )  )
                CSVData.to_json( resultPath )
