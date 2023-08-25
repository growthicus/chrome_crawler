post_crawler: 
	curl -X POST http://0.0.0.0:5001/start -H 'Content-Type: application/json' -d '{"url":"https://ventilation.se/","crawl_id":"asd123", "extractor":"ventilation", "crawler_settings":{}}'

post_chrome: 
	curl -X POST http://0.0.0.0:5000/render -H 'Content-Type: application/json' -d '{"url":"https://liminity.se"}'
