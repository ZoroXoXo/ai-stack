#validates model service behavior

import pytest

from laptop_copilot.services import ollama_client


def test_parse_intent_raises_when_no_model_configured(monkeypatch):
    from laptop_copilot.config import settings

    monkeypatch.setattr(settings, "controller_model", "none")
    with pytest.raises(RuntimeError):
        ollama_client.parse_intent_with_model("open firefox")