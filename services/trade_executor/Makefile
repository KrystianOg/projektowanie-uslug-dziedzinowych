.PHONY: compile get_message test-connection test-send-signal rabbitmq-status check-queue rabbitmq-logs test-all

CONSUME_QUEUE = raw_data_queue
RABBIT_MGMT_API = http://localhost:15672/api/queues/%2F/$(CONSUME_QUEUE)/get

compile:
	uv pip compile pyproject.toml -o requirements.txt

# Check if RabbitMQ is responding
test-connection:
	@echo "Testing RabbitMQ connection..."
	@curl -u guest:guest http://localhost:15672/api/overview || echo "RabbitMQ Management API not accessible"

# Check RabbitMQ container status
rabbitmq-status:
	@docker ps | grep rabbitmq

# Send a test signal to the queue
test-send-signal:
	@echo "Sending test signal to queue..."
	@docker exec rabbitmq rabbitmqadmin publish \
		exchange=amq.default \
		routing_key=signal.trade_executor \
		payload='{"symbol": "AAPL","action":"buy","confidence": 0.89, "timestamp": "2025-10-15T16:00:00"}' \
		properties='{"content_type":"application/json","delivery_mode":2}'


# Check queue status and message count
check-queue:
	@echo "Checking queue status..."
	@docker exec rabbitmq rabbitmqctl list_queues name messages consumers

# View RabbitMQ logs
rabbitmq-logs:
	@docker logs rabbitmq --tail 50

# Complete test flow
test-all: rabbitmq-status test-connection check-queue test-send-signal
	@echo "✓ All tests completed"