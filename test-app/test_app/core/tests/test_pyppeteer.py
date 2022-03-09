import pytest


@pytest.mark.pyppeteer
async def test_login(page, webpack_server, oauth_application):
    await page.goto(webpack_server)
    login_button = await page.waitForXPath('//button[contains(., "Login")]')
    await login_button.click()
    # Wait for elements that should only be present if login succeeded
    await page.waitForXPath('//button[contains(., "Logout")]')
    await page.waitForXPath('//a[contains(., "My Images")]')

@pytest.mark.pyppeteer
async def test_foo(page, webpack_server):
    assert 1 == 2