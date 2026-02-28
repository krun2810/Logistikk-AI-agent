from app.tools import categorize_by_keywords, extract_tracking_number


def test_categorize_tracking() -> None:
    assert categorize_by_keywords("Hvor er pakken min?") == "pakke_sporing"
    assert categorize_by_keywords("I want to track my shipment") == "pakke_sporing"


def test_categorize_complaint() -> None:
    assert categorize_by_keywords("Jeg vil klage på leveransen") == "klage"
    assert categorize_by_keywords("Jeg er ikke fornøyd med servicen") == "klage"


def test_categorize_address_change() -> None:
    assert categorize_by_keywords("Jeg vil endre adressen min") == "adresse_endring"
    assert categorize_by_keywords("Jeg skal flytte snart") == "adresse_endring"


def test_categorize_general() -> None:
    assert categorize_by_keywords("Hei, jeg har et spørsmål") == "generell_henvendelse"
    assert categorize_by_keywords("Hello there") == "generell_henvendelse"


def test_extract_tracking_number_found() -> None:
    text = "Pakken min med nummer NO12345678901234567 er borte"
    result = extract_tracking_number(text)
    assert result == "NO12345678901234567"


def test_extract_tracking_number_not_found() -> None:
    text = "Jeg har ikke noe sporingsnummer"
    result = extract_tracking_number(text)
    assert result is None
