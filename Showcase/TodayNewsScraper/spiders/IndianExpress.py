import sys
import scrapy
import re
from datetime import datetime, timedelta

stopScraping = False
storyCount = 0
storyLimit = 15
daysToScrape = 1

class IndianexpressSpider(scrapy.Spider):
    name = "IndianExpress"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/latest-news/page/1/"]

    def parse(self, response):
        #currPageNum = int( response.css("ul.page-numbers>li>a.currentpage::text").extract_first() )
        global storyCount
        global stopScraping
        
        Links = response.css("div.articles div.title a::attr(href)").extract()
        for Link in Links:
            if( stopScraping == False ):
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
                if( storyCount == storyLimit ):
                    stopScraping = True
                
            else:
                break

        if( stopScraping == False ):
            nextPageLink = response.css( "ul.page-numbers>li:last-of-type>a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)
            
    def parseNews(self, response):
        global stopScraping
        storyLink = response.url      

        headLine = response.css("div.heading-part h1.native_story_title::text").extract_first() or ""
        
        Source = "The Indian Express"
        sourceLink = "https://www.indianexpress.com/"

        imageLink = response.css( "div.full-details span.custom-caption noscript img::attr(src)" ).extract_first() or ""

        contentList = response.css( "div.full-details p::text" ).extract()
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
        articleTiming = response.css( "span[itemprop='dateModified']::attr(content)" ).extract_first()
        articleTiming = re.search( "\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d", articleTiming )[0]
        articleTiming = datetime.strptime( articleTiming, "%Y-%m-%dT%H:%M:%S" )
        if(
            articleTiming < (  rightNow - timedelta( days = daysToScrape )  )
        ):
            stopScraping = True
            
        yield Output
