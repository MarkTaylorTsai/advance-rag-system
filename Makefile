.PHONY: check-rag
check-rag:
	@echo "Running RAG System isolation check..."
	@python3 tests/check_rag_isolation.py
