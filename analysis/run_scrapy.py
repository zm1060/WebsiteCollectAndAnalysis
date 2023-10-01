from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from analysis.count_redirect_or_direct_https import LinkAnalyzerSpider

# Specify the directory containing the HTML files

# Create a Scrapy crawler process
process = CrawlerProcess(get_project_settings())

# Start the crawler with the LinkAnalyzerSpider spider and pass the directory argument
process.crawl(LinkAnalyzerSpider)

# Run the crawler
process.start()