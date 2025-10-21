.PHONY: test-integration test-e2e compile-all

# placeholders for tests scripts
test-integration: 
	@echo "Test integration"

test-e2e:
	@echo "Test e2e"

test-health:
	@echo "Quick smoke test"

# Compile requirements.txt for all services containing uv.lock
compile-all:
	find services -type f -name "uv.lock" -execdir uv pip compile pyproject.toml -o requirements.txt \;

