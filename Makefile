post_crawler: 
	curl -X POST http://0.0.0.0:5001/start -H 'Content-Type: application/json' -d '{"url":"https://www.filterpunkten.se/product/1342/flexit-spirit-uni-2-filter-f7--f7","crawl_id":"asd123", "extractor":"ventilation", "crawler_settings":{"extract_url_contain":["product"], "follow_url_contain":["category", "product"], "thread_sleep":5}}'

post_chrome: 
	curl -X POST http://0.0.0.0:5000/render -H 'Content-Type: application/json' -d '{"url":"https://liminity.se"}'
