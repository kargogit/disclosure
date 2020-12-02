import sys
import scrapy
import re
from datetime import datetime, timedelta

stopScraping = False
storyCount = 0
storyLimit = 15
daysToScrape = 1

class Gadgets360Spider(scrapy.Spider):
    name = "Gadgets360"
    allowed_domains = ["gadgets.ndtv.com"]
    start_urls = ["https://gadgets.ndtv.com/news/page-1"]

    def parse(self, response):
        #currPageNum = int( response.css("ul.page-numbers>li>a.currentpage::text").extract_first() )
        global storyCount
        global stopScraping

        Links = response.css("div.story_list ul li div.caption_box a:first-of-type::attr(href)").extract()
        for Link in Links:
            if( stopScraping == False ):
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
                if( storyCount == storyLimit ):
                    stopScraping = True
                
            else:
                break

        if( stopScraping == False ):
            nextPageLink = response.css( "div.pagination span + a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)
            
    def parseNews(self, response):
        storyLink = response.url      

        headLine = response.css("div.lead_heading h1::text").extract_first() or ""
        
        Source = "Gadgets360"
        sourceLink = "https://gadgets.ndtv.com/"

        imageLink = response.css( "div.fullstoryImage picture img::attr(src)" ).extract_first() or ""

        contentList = response.css( "div.content_text p *::text" ).extract()
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
        articleTiming = response.css( "div.dateline *::text" ).extract()
        for Element in articleTiming:
            DateTimeMatch = re.search( "\d+ \w+ \d\d\d\d \d+:\d\d", Element )
            if DateTimeMatch is not None:
                articleTiming = DateTimeMatch[0]
                break

        articleTiming = datetime.strptime( articleTiming, "%d %B %Y %H:%M" )
        if(
            articleTiming < (  rightNow - timedelta( days = daysToScrape )  )
        ):
            stopScraping = True

        yield Output
