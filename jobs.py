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


        job_func_selector = "div.selectize-control.ng-isolate-scope.ng-pristine.ng-valid.multi.plugin-remove_button"
        await page.locator(job_func_selector).nth(1).click()
        await page.wait_for_timeout(300)  # Wait for dropdown to open

        job_func_option_selector = "div.option.selectize-option.nested-option"

        target_job_func_arr = ['All-Software Engineering', 'backend development', 'frontend development']
        target_job_func_arr = [normalise_text(t) for t in target_job_func_arr]
        target_job_func_set = set(target_job_func_arr)

        for target_job_func in target_job_func_arr:
            # Re-open the dropdown before each selection
            await page.locator(job_func_selector).nth(1).click()
            await page.wait_for_timeout(300)
            options = await page.query_selector_all(job_func_option_selector)
            found = False

            for opt in options:
                text = await opt.inner_text()
                option_text = normalise_text(text)
                if option_text == target_job_func:
                    try:
                        await opt.scroll_into_view_if_needed()
                        await opt.click()
                        print(f"Clicked '{text}' option.")
                        found = True
                        break
                    except Exception as click_err:
                        print(f"Failed to click '{text}' option: {click_err}")
            if not found:
                print(f"Option matching '{target_job_func}' not found.")























        

    except Exception as e:
        print(f"Error occurred: {e}")

    time.sleep(2)  # Wait for the page to update after clicking

def normalise_text(text):
    return text.replace(' ', '').replace('-', '').lower()