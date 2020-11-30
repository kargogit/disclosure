import os
import sys
import json
import pandas as pd

datasetPath = os.path.join( r"DatasetPrep", r"Dataset" )
JSONPath = os.path.join( datasetPath, r"JSONs" )
firstFilePath = os.path.join( JSONPath, sys.argv[1] )
secondFilePath = os.path.join( JSONPath, sys.argv[2] )
resultFilePath = os.path.join( JSONPath, sys.argv[3] )
firstFileFrame = pd.DataFrame(
    json.load(
        open( file = firstFilePath, mode = 'r', encoding = "utf-8", errors = "ignore" )
    )
)
secondFileFrame = pd.DataFrame(
    json.load(
        open( file = secondFilePath, mode = 'r', encoding = "utf-8", errors = "ignore" )
    )
)

print(firstFileFrame)
print(secondFileFrame)

firstFileFrame = pd.concat(  [ firstFileFrame, secondFileFrame ], ignore_index = True  )
print( firstFileFrame )
print( resultFilePath )
firstFileFrame.to_json( resultFilePath )
