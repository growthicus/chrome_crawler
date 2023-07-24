api_dev:
	flask --app server/api run

api_dev_post:
	curl -X POST http://127.0.0.1:5000/render -H 'Content-Type: application/json' -d '{"url":"https://www.liminity.se"}'
