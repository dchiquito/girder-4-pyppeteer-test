import pytest


@pytest.mark.pyppeteer
async def test_foo(page, webpack_server):
    print(page)
    print(webpack_server)
    assert 1 == 2
