# AirScraper
Scrapes the Jetblue website for information about its flights, costs, and reward point values, exports to .csv!

## Usage
Download AirScraper and make sure you have Scrapy (and its dependencies) installed!
Navigate to the AirScraper folder and run AirScraper using the following format:
```
scrapy crawl airSpider -a args=MCO,JFK,2015-05-13,2015-05-15
```

* arg0: Origin Airport Code
* arg1: Destination Airport Code
* arg2: Departure Date
* arg3: Return Date

##Output
A file named `Output.csv` will be generated in the AirScraper directory
