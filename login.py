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
        await page.wait_for_timeout(1000)  # Wait 1 second for scripts to settle
        await page.wait_for_selector('#email', timeout=5000)
        await page.wait_for_selector('#password', timeout=5000)
        # Use type() for more reliable input
        await page.click('#email')
        await page.type('#email', email, delay=50)
        await page.click('#password')
        await page.type('#password', password, delay=50)
        await page.wait_for_timeout(500)  # Small delay before clicking login
        # Click login and wait for navigation or sign out button, with a 5-second timeout
        try:
            async with page.expect_navigation(timeout=5000):
                await page.click('button[type="submit"].btn-success')
        except Exception:
            # Navigation may not always happen, so continue
            await page.click('button[type="submit"].btn-success')
        print("Login attempted!")
        login_success = False
        try:
            # Wait up to 5 seconds for either the opportunities page or sign out button
            await page.wait_for_function(
                "window.location.href.startsWith('https://www.instahyre.com/candidate/opportunities') || document.querySelector('a#nav-candidates-logout[href=\'/logout/\']') !== null",
                timeout=5000
            )
            current_url = page.url
            if current_url.startswith("https://www.instahyre.com/candidate/opportunities"):
                print("Login successful! Redirected to opportunities page.")
                login_success = True
            else:
                print("Login successful! Sign out button found.")
                login_success = True
        except Exception:
            print("Login failed or not redirected within 5 seconds.")
        await browser.close()

        if not login_success:
            print("Login failed. Please check your credentials or the website's response.")
        else:
            print("Login process completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
