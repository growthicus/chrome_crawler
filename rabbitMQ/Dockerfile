# Use the official RabbitMQ image as the base image
FROM rabbitmq:3-management

# Enable the RabbitMQ plugins you want here
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp
