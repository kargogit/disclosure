import sys
import scrapy
import re
from datetime import datetime, timedelta

stopScraping = False
storyCount = 0
storyLimit = 15
daysToScrape = 1

paginationPrefix = "https://www.dailypioneer.com/top-stories/page/"

class ThepioneerSpider(scrapy.Spider):
    name = "ThePioneer"
    allowed_domains = ["dailypioneer.com"]
    start_urls = ["https://www.dailypioneer.com/top-stories/page/1"]

    def parse(self, response):
        #currPageNum = int( response.css("ul.page-numbers>li>a.currentpage::text").extract_first() )
        global storyCount
        global stopScraping

        Links = response.css(  "div.col-sm div.highLightedNews div.row div.col-md-4 ul.list-unstyled li h3 a::attr( href )"  ).extract()
        Links = Links + response.css(  "div.col-sm div.innerNewsList div.row div.col-sm-9 h2 a::attr( href )"  ).extract()
        urlPrefix = "https://www.dailypioneer.com"
        for Link in Links:
            if( stopScraping == False ):
                Link = urlPrefix + Link
                yield scrapy.Request(Link, callback = self.parseNews)
                storyCount += 1
                if( storyCount == storyLimit ):
                    stopScraping = True
                
            else:
                break

        if( stopScraping == False ):
            nextPageLink = paginationPrefix + response.css( "div.pagingList ul li.current + li a::attr(href)" ).extract_first()
            #TODO Add check for nextPageLink in order to catch last page
            yield scrapy.Request(nextPageLink, callback = self.parse)
            
    def parseNews(self, response):
        global stopScraping
        storyLink = response.url      

        headLine = response.css("div.storyDetailBox div.row div.col-12 h2[ itemprop = 'headline' ]::text").extract_first() or ""
        
        Source = "The Pioneer"
        sourceLink = "https://www.dailypioneer.com/"

        imageLink = response.css( "div.storyDetailBox div.row div.col-12 div.bodyContentSection div#printArea div.newsImgBox img::attr(src)" ).extract_first() or ""

        contentList = response.css( "div.storyDetailBox div.row div.col-12 div.bodyContentSection div#printArea div.newsDetailedContent p::text" ).extract()
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
        articleTiming = response.css( "div.storyDetailBox div.row div.col-12 div.row div.col div.newsInfo span[ itemprop = 'dateModified' ]::attr(content)" ).extract_first()
        articleTiming = datetime.strptime( articleTiming, "%A, %d %B %Y" )
        if(
            articleTiming < (  rightNow - timedelta( days = daysToScrape )  )
        ):
            stopScraping = True
            
        yield Output

