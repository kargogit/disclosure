import os
import sys
import json
import pandas as pd

firstFilePath = sys.argv[1]
secondFilePath = sys.argv[2]
resultFilePath = sys.argv[3]

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

firstFileFrame = pd.concat(  [ firstFileFrame, secondFileFrame ], ignore_index = True  ).reset_index( drop = True )
print( firstFileFrame )
print( resultFilePath )
firstFileFrame.to_json( resultFilePath )
