post_crawler: 
	curl -X POST http://0.0.0.0:5001/start -H 'Content-Type: application/json' -d '{"url":"https://stadium.se","crawl_id":"asd123", "crawler_settings": {"url_not_contain":["*", "#"]}, "server_settings": {"reciever_host":"http://crawler", "reciever_port":"5000"}}'

post_chrome: 
	curl -X POST http://0.0.0.0:5000/render -H 'Content-Type: application/json' -d '{"url":"https://liminity.se"}'
