# ChromeCrawler

Simple threaded crawler using headless chrome to render pages through a small flask API.

## Installation

1. Git clone this repo
2. sudo docker-compose up --build
3. Send request to crawler API to start crawling 
   - See Makefile for example post (make post_crawler)
     - See CrawlerSettings in settings.py