FROM rabbitmq:3-management

RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

COPY rabbitmq_definitions.json /etc/rabbitmq/rabbitmq_definitions.json.template

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}
ENV RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS}
ENV RABBITMQ_DEFAULT_VHOST=${RABBITMQ_DEFAULT_VHOST}

ENTRYPOINT ["/entrypoint.sh"]
