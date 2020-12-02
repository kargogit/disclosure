import sys
import scrapy
import re
from datetime import datetime, timedelta

stopScraping = False
storyCount = 0
storyLimit = 15
daysToScrape = 1

urlPrefix = "https://www.hindustantimes.com/latest-news/"

class HindtimesSpider(scrapy.Spider):
    name = "HindTimes"
    allowed_domains = ["hindustantimes.com"]
    start_urls = ["https://www.hindustantimes.com/latest-news/"]

    def parse(self, response):
        #currPageNum = int( response.css("ul.page-numbers>li>a.currentpage::text").extract_first() )
        global storyCount
        global stopScraping

        Links = response.css("ul.more-latest-news li div div.media-body div.media-heading a::attr(href)").extract()
        for Link in Links:
            if( stopScraping == False ):
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
                if( storyCount == storyLimit ):
                    stopScraping = True
                
            else:
                break

        if( stopScraping == False ):
            nextPageLink = urlPrefix + response.css( "div.pagination ul li.fl:last-of-type a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)
            
    def parseNews(self, response):
        storyLink = response.url      

        headLine = response.css("div.article div.col9 div.storyArea h1::text").extract_first() or ""
        
        Source = "Hindustan Times"
        sourceLink = "https://www.hindustantimes.com/"

        imageLink = response.css( "div.article div.col9 div.storyArea figure img::attr(src)" ).extract_first() or ""

        contentList = response.css( "div.article div.col9 div.storyArea div.storyDetail p::text" ).extract()
        Content = " ".join( contentList )

        Output = {
            "headLine": headLine,
            "storyLink": storyLink,
            "Source": Source,
            "sourceLink": sourceLink,
            "imageLink": imageLink,
            "Content": Content
        }

        rightNow = datetime.now()
        articleTiming = response.css( "div.article div.col9 div.storyArea span.text-dt::text" ).extract_first()
        articleTiming = re.sub( "Updated:\s+", "", articleTiming )
        articleTiming = re.sub( "\sIST", "", articleTiming )
        articleTiming = datetime.strptime( articleTiming, "%b %d, %Y, %H:%M" )
        if(
            articleTiming < (  rightNow - timedelta( days = daysToScrape )  )
        ):
            stopScraping = True

        yield Output
