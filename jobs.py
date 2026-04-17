from playwright.async_api import Page
import time

async def handle_jobs(page: Page):
    # Define the selector for the 'Search other jobs' element
    selector = "div.job-search-heading:has(h6:text('Search other jobs'))"
    await page.wait_for_selector(selector, timeout=5000)
    parent_div = await page.query_selector(selector)
    try:
        await parent_div.click()
        print("Clicked 'Search other jobs' heading.")

        await page.click('#years')
        await page.type('#years', '2', delay=10)


        job_func_selector = "input[placeholder='Select job functions']"
        await page.wait_for_selector(job_func_selector, timeout=1000)
        await page.click(job_func_selector)

        # Click the dropdown option with text 'All - Software Engineering', insensitive to case, spaces, and hyphens
        # Normalize text in JS: remove spaces, hyphens, lowercase
        option_selector = (
            "div.option.selectize-option.nested-option"
        )
        await page.wait_for_selector(option_selector, timeout=1000)
        option = await page.query_selector(f"{option_selector}")
        # Find the correct option by evaluating all options
        options = await page.query_selector_all(option_selector)
        target_text = 'All-Software Engineering'
        target_text = normalise_text(target_text)
        clicked = False
        for opt in options:
            text = await opt.inner_text()
            print(f"Option text: '{text}'")
            norm = normalise_text(text)
            if norm == target_text:
                await opt.click()
                print("Clicked 'All - Software Engineering' option.")
                clicked = True
        if not clicked:
            print("Option 'All - Software Engineering' not found.")

    except Exception as e:
        print(f"Error occurred: {e}")

    time.sleep(2)  # Wait for the page to update after clicking

def normalise_text(text):
    return text.replace(' ', '').replace('-', '').lower()