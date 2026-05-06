from app.services.start import get_start_text


def test_get_start_text() -> None:
    result: str = get_start_text()

    assert result == 'Hello!'