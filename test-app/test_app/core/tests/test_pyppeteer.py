import pytest


@pytest.mark.pyppeteer
async def test_login(page, webpack_server):
    from asyncio import gather
    await page.goto(webpack_server)
    await page.waitFor(2_000)
    print(dir(page))
    login_button = await page.waitForXPath('//button[contains(., "Login")]')
    await login_button.click()
    await page.waitFor(5_000)
    assert 1 == 2
