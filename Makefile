.PHONY: check-rag
check-rag:
	@echo "Running RAG System isolation check..."
	@python3 tests/check_rag_isolation.py

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	@docker-compose -f docker-compose.test.yml up --build --exit-code-from tests
	@docker-compose -f docker-compose.test.yml down
