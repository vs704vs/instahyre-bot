import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

_browser = None
_playwright = None

async def login_main():
    global _browser, _playwright
    load_dotenv()
    email = os.getenv("INSTAHYRE_EMAIL")
    password = os.getenv("INSTAHYRE_PASSWORD")
    if not email or not password:
        print("Email or password not set in environment variables.")
        return None, None

    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-setuid-sandbox",
            "--disable-software-rasterizer",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-sync",
            "--disable-translate",
            "--metrics-recording-only",
            "--mute-audio",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--disable-accelerated-2d-canvas",
            "--disable-webgl",
            "--hide-scrollbars",
            "--ignore-certificate-errors",
        ]
    )
    context = await _browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    try:
        await page.goto("https://www.instahyre.com/login/", timeout=60000, wait_until="domcontentloaded")
    except Exception as nav_err:
        print(f"Navigation error: {nav_err}")
        await page.screenshot(path="/tmp/nav_error.png")
        raise
    await page.wait_for_timeout(3000)
    await page.wait_for_selector('#email', timeout=20000)
    await page.wait_for_selector('#password', timeout=20000)
    await page.click('#email')
    await page.type('#email', email, delay=10)
    await page.click('#password')
    await page.type('#password', password, delay=10)
    await page.wait_for_timeout(50)
    await page.click('button[type="submit"].btn-success')
    print("Login attempted!")
    await page.wait_for_timeout(5000)
    print(f"Current URL after login: {page.url}")
    await page.screenshot(path="/tmp/after_login.png")
    print(f"Page title: {await page.title()}")

    login_success = False
    try:
        await page.wait_for_function(
            "window.location.href.startsWith('https://www.instahyre.com/candidate/opportunities') || document.querySelector(\"a#nav-candidates-logout[href='/logout/']\") !== null",
            timeout=30000
        )
    except Exception as wait_err:
        print(f"Wait for login redirect failed: {wait_err}")
        print(f"Final URL: {page.url}")
        await page.screenshot(path="/tmp/login_failed.png")
        return None, None
    signout_button = await page.query_selector("a#nav-candidates-logout[href='/logout/']")
    if signout_button:
        login_success = True

    if not login_success:
        print("Login failed. Please check your credentials or the website's response.")
    else:
        print("Login process completed successfully.")

    return page, _browser

async def close_browser():
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None
