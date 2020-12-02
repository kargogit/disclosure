from os import system

system("scrapy crawl Gadgets360 -o ScrapedDataG360.json")

system("scrapy crawl HindTimes -o ScrapedDataHT.json")

system("scrapy crawl IndianExpress -o ScrapedDataIE.json")

system("scrapy crawl ThePioneer -o ScrapedDataTP.json")

system("python3 PrepareJSON.py")

system("python3 Classify.py")