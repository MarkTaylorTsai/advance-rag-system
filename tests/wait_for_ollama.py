#!/usr/bin/env python3
"""Wait for Ollama model to be available."""
import json
import time
import sys
import urllib.request

def has_model():
    try:
        with urllib.request.urlopen('http://localhost:11434/api/tags', timeout=5) as r:
            payload = json.loads(r.read().decode('utf-8'))
            for model in payload.get('models', []):
                name = model.get('name', '')
                # Check for exact match or name with tag (e.g., 'nomic-embed-text:latest')
                if name == 'nomic-embed-text' or name.startswith('nomic-embed-text:'):
                    print(f"Found model: {name}")
                    return True
    except Exception as e:
        print(f"Waiting for Ollama... ({e})")
    return False

for i in range(60):
    if has_model():
        print('Model found!')
        sys.exit(0)
    time.sleep(2)
else:
    print('ERROR: Ollama model not available after wait.')
    sys.exit(1)

