#!/bin/bash

envsubst < /etc/rabbitmq/rabbitmq_definitions.json.template > /etc/rabbitmq/rabbitmq_definitions.json

rabbitmq-server &

sleep 10

rabbitmqctl import_definitions /etc/rabbitmq/rabbitmq_definitions.json

rabbitmqctl stop_app

rabbitmqctl start_app

tail -f /dev/null
