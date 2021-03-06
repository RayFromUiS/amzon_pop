from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.log import configure_logging

from amzon.spiders.amzon_spider import AmzonPopularSpider,AmzonTelsaSpider


from scrapy.settings import Settings
from amzon import settings


def run_scraper():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    configure_logging()
    # runner = CrawlerRunner(settings=crawler_settings)
    # task = LoopingCall(lambda: runner.crawl(NewsOeOffshoreSpider))
    # task.start(6000 * 100)
    # reactor.run()
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AmzonTelsaSpider)
    # process = CrawlerProcess(settings=crawler_settings)
    # process.cnPopularSpider)
    #
    # process.start()


if __name__ == "__main__":
    run_scraper()
