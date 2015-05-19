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
NOTE: The current default output (if run without args specified) is for MCO->BOS on 2015-05-13 to 2015-05-15

##Goals
Airscraper was originally just a quick weekend project to get some experience with Python and the Scrapy framework.  As such, it currently only grabs the flight info from one set of origins/destinations at a time, and only for the dates that the user specifies.  I would like to expand this to correctly grab information on every Jetblue flight for the coming X user-entered days.
