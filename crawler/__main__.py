from time import sleep

from .crawler import Crawler

if __name__ == "__main__":

    sleep(5)

    crw = Crawler()

    crw.crawl_grades()
