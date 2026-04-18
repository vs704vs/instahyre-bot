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
    _browser = await _playwright.chromium.launch(headless=False)
    page = await _browser.new_page()
    await page.goto("https://www.instahyre.com/login/")
    await page.wait_for_load_state('networkidle')
    await page.wait_for_selector('#email', timeout=5000)
    await page.wait_for_selector('#password', timeout=5000)
    await page.click('#email')
    await page.type('#email', email, delay=10)
    await page.click('#password')
    await page.type('#password', password, delay=10)
    await page.wait_for_timeout(50)
    await page.click('button[type="submit"].btn-success')
    print("Login attempted!")

    login_success = False
    await page.wait_for_function(
        "window.location.href.startsWith('https://www.instahyre.com/candidate/opportunities') || document.querySelector(\"a#nav-candidates-logout[href='/logout/']\") !== null",
        timeout=5000
    )
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
