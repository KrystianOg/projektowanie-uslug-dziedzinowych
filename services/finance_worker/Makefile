.PHONY: compile, get_message

CONSUME_QUEUE = raw_data_queue
RABBIT_MGMT_API = http://localhost:15672/api/queues/%2F/$(CONSUME_QUEUE)/get

compile:
	uv pip compile pyproject.toml -o requirements.txt

get_message:
	curl -i -u guest:guest -H "Content-Type: application/json" -X POST $(RABBIT_MGMT_API) -d '{"count": 1,"requeue": true,"encoding": "auto","truncate": 50000,"ackmode": "ack_requeue_false"}'
