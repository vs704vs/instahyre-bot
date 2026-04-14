from playwright.async_api import Page

async def handle_jobs(page: Page):
    # Define the selector for the 'Search other jobs' element
    selector = "div.job-search-heading:has(h6:text('Search other jobs'))"
    await page.wait_for_selector(selector, timeout=5000)
    parent_div = await page.query_selector(selector)
    if parent_div:
        await parent_div.click()
        print("Clicked 'Search other jobs' heading.")
    else:
        print("'Search other jobs' heading not found.")
