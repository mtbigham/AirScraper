import scrapy
from scrapy.http.request import Request
from AirScraper.items import AirscraperItem
import datetime

#scrapy crawl airSpider -a args=MCO,JFK,2015-05-13,2015-05-15 -o test.csv

class airSpider(scrapy.Spider):
	name = "airSpider"
	start_urls = ["https://book.jetblue.com"]
	#defaults
	origin = "MCO"
	dest = "BOS"
	dateDep = "2015-05-13"
	dateRet = "2015-05-15"
	
	def __init__(self, category=None, args=""):
		user_input = args.split(',')
		self.origin = user_input[0]
		self.dest = user_input[1]
		self.dateDep = user_input[2]
		self.dateRet = user_input[3]
	
	def parse(self, response):
		#perform first search for most information		
		yield scrapy.FormRequest.from_response(
			response,
			formname = "searchForm",
			formdata={'origin' : self.origin, 'destination' : self.dest, 'departureDate' : self.dateDep, 'returnDate' : self.dateRet},
			callback=self.after_search1
		)
		
		
		#perform second search for points!
		yield scrapy.FormRequest.from_response(
			response,
			formname = "searchForm",
			formdata={'origin' : self.origin, 'destination' : self.dest, 'departureDate' : self.dateDep, 'returnDate' : self.dateRet, 'fareType': "TRUEBLUE"},
			callback=self.after_search2
		)
		
		
	def after_search1(self, response):
		#from scrapy.shell import inspect_response
		#inspect_response(response)
		
		flights = response.xpath('//*[contains(@class, "flight-row no-mint")]')
		
		for sel in flights:
			flightInfo = sel.xpath('.//div[1]/div[1]/div[4]')
			flightNum = flightInfo.xpath('.//div[1]/a/text()').extract()
			#check if we're looking at a valid flight (avoid the header 'flight-row' classes)
			if flightNum:
				#create new item
				item = AirscraperItem()
				
				#set flightNum (for layovers, this is only the FIRST flight's number)
				item['flightNum'] = flightNum
				
				#if there's a class named "layover", we've gotta account for layover format!
				#check for layover
				layover = sel.xpath('.//div/*[contains(@class, "layover")]')
				if layover:
					#use layover formatting (from = origin, to = FINAL destination)
					fromVals = sel.xpath('.//div[1]/div[1]/div[1]')
					toVals = sel.xpath('.//div[1]/div[last()]/div[3]')
					
				else:
					#ignore layover formatting
					fromVals = sel.xpath('.//div[1]/div[1]/div[1]')
					toVals = sel.xpath('.//div[1]/div[1]/div[3]')
					
				#get time and departure city from fromVals
				item['departTime'] = fromVals.xpath('.//time/text()').extract()
				item['depart'] = fromVals.xpath('.//span[1]/text()').extract()
				
				#get time and arrival city from toVals
				item['arriveTime'] = toVals.xpath('.//time/text()').extract()
				item['dest'] = toVals.xpath('.//span[1]/text()').extract()
				
				#get price
				price = sel.xpath('.//*[contains(@class, "fare box non-refund")]/div[2]/span[2]/text()').extract()
				#unsure what's going on here, always got 'index out of bounds' error when attempting to strip index 0
				for i, v in enumerate(price):
					item['price'] = v.strip()
				
				#determine if we're leaving or returning
				if item['depart'][0] == self.origin: #we're leaving
					#set depart date and determine arrival date
					item['departDate'] = self.dateDep
					
					#if we land the next day, update the arriveDate accordingly
					nextDay = sel.xpath('.//div[1]/div[last()]/div[3]/*[contains(@class, "next-day")]/text()')
					if nextDay:
						originalDate = datetime.datetime.strptime(self.dateDep, "%Y-%m-%d")
						newDate = originalDate + datetime.timedelta(days=1)
						item['arriveDate'] = newDate.strftime("%Y-%m-%d")
					else:
						item['arriveDate'] = self.dateDep
				else: #we're returning
					#set depart date to the selected return date and determine arrival date
					item['departDate'] = self.dateRet
					
					#if we land the next day, update the arriveDate accordingly
					nextDay = sel.xpath('.//div[1]/div[last()]/div[3]/*[contains(@class, "next-day")]/text()')
					if nextDay:
						originalDate = datetime.datetime.strptime(self.dateRet, "%Y-%m-%d")
						newDate = originalDate + datetime.timedelta(days=1)
						item['arriveDate'] = newDate.strftime("%Y-%m-%d")
					else:
						item['arriveDate'] = self.dateRet
					
				yield item
				
	def after_search2(self, response):
		#from scrapy.shell import inspect_response
		#inspect_response(response)
		
		flights = response.xpath('//*[contains(@class, "flight-row no-mint")]')
		
		for sel in flights:
			flightInfo = sel.xpath('.//div[1]/div[1]/div[4]')
			flightNum = flightInfo.xpath('.//div[1]/a/text()').extract()
			#check if we're looking at a valid flight (avoid the header 'flight-row' classes)
			if flightNum:
				#create new item
				item = AirscraperItem()
				
				#set flightNum (for layovers, this is only the FIRST flight's number)
				item['flightNum'] = flightNum
				
				#if there's a class named "layover", we've gotta account for layover format!
				#check for layover
				layover = sel.xpath('.//div/*[contains(@class, "layover")]')
				if layover:
					#use layover formatting (from = origin, to = FINAL destination)
					fromVals = sel.xpath('.//div[1]/div[1]/div[1]')
					toVals = sel.xpath('.//div[1]/div[last()]/div[3]')
					
				else:
					#ignore layover formatting
					fromVals = sel.xpath('.//div[1]/div[1]/div[1]')
					toVals = sel.xpath('.//div[1]/div[1]/div[3]')
					
				#get time and departure city from fromVals
				item['departTime'] = fromVals.xpath('.//time/text()').extract()
				item['depart'] = fromVals.xpath('.//span[1]/text()').extract()
				
				#get time and arrival city from toVals
				item['arriveTime'] = toVals.xpath('.//time/text()').extract()
				item['dest'] = toVals.xpath('.//span[1]/text()').extract()
				
				#get points
				points = sel.xpath('.//*[contains(@class, "fare box non-refund")]/div[2]/span[2]/text()').extract()
				item['points'] = points[0].split()[0]

				
				#determine if we're leaving or returning
				if item['depart'][0] == self.origin: #we're leaving
					#set depart date and determine arrival date
					item['departDate'] = self.dateDep
					
					#if we land the next day, update the arriveDate accordingly
					nextDay = sel.xpath('.//div[1]/div[last()]/div[3]/*[contains(@class, "next-day")]/text()')
					if nextDay:
						originalDate = datetime.datetime.strptime(self.dateDep, "%Y-%m-%d")
						newDate = originalDate + datetime.timedelta(days=1)
						item['arriveDate'] = newDate.strftime("%Y-%m-%d")
					else:
						item['arriveDate'] = self.dateDep
				else: #we're returning
					#set depart date to the selected return date and determine arrival date
					item['departDate'] = self.dateRet
					
					#if we land the next day, update the arriveDate accordingly
					nextDay = sel.xpath('.//div[1]/div[last()]/div[3]/*[contains(@class, "next-day")]/text()')
					if nextDay:
						originalDate = datetime.datetime.strptime(self.dateRet, "%Y-%m-%d")
						newDate = originalDate + datetime.timedelta(days=1)
						item['arriveDate'] = newDate.strftime("%Y-%m-%d")
					else:
						item['arriveDate'] = self.dateRet
					
				yield item