# validates retrieval and storage logic

import pytest

from laptop_copilot import router


def test_open_app_routes():
    intent = router.route("open firefox")
    assert intent.tool_name == "open_app"
    assert intent.args == {"app_name": "firefox"}


def test_create_note_routes():
    intent = router.route("note: buy milk")
    assert intent.tool_name == "create_note"
    assert intent.args == {"text": "buy milk"}


def test_recent_files_routes_with_limit():
    intent = router.route("recent files 5")
    assert intent.tool_name == "show_recent_files"
    assert intent.args == {"limit": 5}


def test_recent_files_routes_without_limit():
    intent = router.route("recent files")
    assert intent.tool_name == "show_recent_files"
    assert intent.args == {}


def test_open_last_file_routes():
    intent = router.route("open last download")
    assert intent.tool_name == "open_last_file"


def test_calendar_routes():
    intent = router.route("calendar")
    assert intent.tool_name == "open_calendar"


def test_clipboard_routes():
    intent = router.route("clipboard search invoice")
    assert intent.tool_name == "show_clipboard"
    assert intent.args == {"query": "invoice"}


def test_device_status_routes():
    intent = router.route("battery")
    assert intent.tool_name == "device_status"


def test_unroutable_request_raises():
    with pytest.raises(router.UnroutableRequest):
        router.route("do something completely unsupported and vague")