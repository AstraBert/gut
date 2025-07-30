from src.gut._banner import _show_banner, _banner


def test_banner() -> None:
    try:
        success = True
        assert _show_banner() == _banner
    except Exception as e:
        if isinstance(e, AssertionError):
            raise AssertionError("Returned banner and actual banner are not equal")
        else:
            success = False
    assert success
