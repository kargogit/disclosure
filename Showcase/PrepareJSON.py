import os
import json
import re
import pandas as pd

def main():
    JSONData = ""
    with open( file="ScrapedData.json", mode="r", encoding="utf-8", errors="ignore" ) as txtFile:
        JSONData = txtFile.read()
    JSONData = re.sub( "\]\[", ',', JSONData )
    with open(file="ScrapedData.json", mode="w", encoding="utf-8") as txtFile:
        txtFile.write(JSONData)

    JSONData = json.load(  open( file = "ScrapedData.json", mode = "r", encoding = "utf-8", errors = "ignore" )  )
    JSONData = pd.DataFrame(JSONData)

    for rowNum in range( JSONData.shape[0] ):
        rowFrame = JSONData.iloc[rowNum]
        if( rowFrame["Content"] != "" and rowFrame["headLine"] != "" and rowFrame["imageLink"] != "" ):
            filePath = os.path.join( "IndividualScrapedData", str( rowNum ) + ".json" )
            rowFrame.to_json( filePath )
            
            with open( file = filePath, mode = "r", encoding = "utf-8", errors = "ignore" ) as txtFile:
                rowFrame = txtFile.read()
            rowFrame = re.sub( "\\\/", '/', rowFrame )
            with open( file = filePath, mode = "w", encoding = "utf-8" ) as txtFile:
                txtFile.write(rowFrame)

if __name__ == "__main__":
    main()