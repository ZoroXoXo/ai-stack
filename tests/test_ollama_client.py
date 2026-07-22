#validates model service behavior

import httpx
import pytest

from laptop_copilot.services import ollama_client


def test_parse_intent_raises_when_no_model_configured(monkeypatch):
    from laptop_copilot.config import settings

    monkeypatch.setattr(settings, "controller_model", "none")
    with pytest.raises(RuntimeError):
        ollama_client.parse_intent_with_model("open firefox")


def test_parse_intent_falls_back_when_model_does_not_support_tools(monkeypatch):
    class MockResponse:
        def __init__(self, text: str):
            self._text = text

        def raise_for_status(self):
            raise httpx.HTTPStatusError(
                "tool support error",
                request=httpx.Request("POST", "http://test"),
                response=httpx.Response(400, content=self._text.encode("utf-8")),
            )

        @property
        def text(self) -> str:
            return self._text

    class MockClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def post(self, *args, **kwargs):
            return MockResponse(
                "Model registry.ollama.ai/library/phi3.5:3.8b-mini-instruct-q4_K_M does not support tools"
            )

    monkeypatch.setattr(httpx, "Client", MockClient)
    result = ollama_client.parse_intent_with_model(
        "open firefox", model="phi3.5:3.8b-mini-instruct-q4_K_M"
    )
    assert result == {"tool_name": None, "args": {}}
