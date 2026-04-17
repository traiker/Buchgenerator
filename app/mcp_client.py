from __future__ import annotations

import requests


class MCPRestClient:
    def __init__(self, endpoint: str, timeout_seconds: int = 20):
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    def query(self, question: str) -> str:
        response = requests.post(
            self.endpoint,
            json={"question": question},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        return str(data.get("answer", ""))
