import os
import sys
import json
import pandas as pd
import random

filePath = sys.argv[1]
resultPath = sys.argv[3]
rowCount = int( sys.argv[2] )

fileFrame = pd.DataFrame(
    json.load(
        open( file = filePath, mode = 'r', encoding = "utf-8", errors = "ignore" )
    )
)
fileFrame.reset_index( inplace = True, drop = True )
print(fileFrame)
frameRowCount = fileFrame.shape[0]

if( rowCount < frameRowCount ):
    randomRowSeq = random.sample( range(frameRowCount), rowCount )
    newRandomFrame = fileFrame[  fileFrame.index.isin( randomRowSeq )  ]
    newRandomFrame.reset_index( inplace = True, drop = True )
    print(newRandomFrame)
    newRandomFrame.to_json( resultPath )