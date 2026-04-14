import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

async def main():
    # Load environment variables from .env file
    load_dotenv()
    email = os.getenv("INSTA_EMAIL")
    password = os.getenv("INSTA_PASSWORD")
    if not email or not password:
        print("Email or password not set in environment variables.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.instahyre.com/login/")
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(500)  # Wait 0.5 second for scripts to settle
        await page.wait_for_selector('#email', timeout=50)
        await page.wait_for_selector('#password', timeout=50)
        await page.click('#email')
        await page.type('#email', email, delay=10)
        await page.click('#password')
        await page.type('#password', password, delay=10)
        await page.wait_for_timeout(50)
        # Click login button
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

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
