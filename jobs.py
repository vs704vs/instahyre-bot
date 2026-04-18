from playwright.async_api import Page
import time
import os
from dotenv import load_dotenv

async def handle_jobs(page: Page):
    load_dotenv()
    target_yoe = os.getenv("YOE", "")

    target_job_func_string = os.getenv("JOB_FUNCTIONS", "")
    target_job_func_arr = target_job_func_string.split(",") if target_job_func_string else []

    target_location_string = os.getenv("LOCATIONS", "")
    target_location_arr = target_location_string.split(",") if target_location_string else []

    target_company_size = os.getenv("COMPANY_SIZE", "")

    selector = "div.job-search-heading:has(h6:text('Search other jobs'))"
    await page.wait_for_selector(selector, timeout=5000)

    try:
        # Only click the heading if the filter panel is not already open
        years_visible = await page.locator('#years:not([disabled])').is_visible()
        if not years_visible:
            await page.evaluate("""
                () => {
                    const headings = document.querySelectorAll('div.job-search-heading');
                    for (const el of headings) {
                        if (el.textContent.trim().includes('Search other jobs')) {
                            el.click();
                            break;
                        }
                    }
                }
            """)
            await page.wait_for_selector('#years:not([disabled])', state='visible', timeout=10000)
        print("Clicked 'Search other jobs' heading.")

        await filter_jobs_by_yoe(page, target_yoe)
        await filter_jobs_by_job_function(page, target_job_func_arr)
        await filter_jobs_by_location(page, target_location_arr)
        await filter_jobs_by_size(page, target_company_size)
        await page.click("#show-results")

    except Exception as e:
        print(f"Error occurred: {e}")




async def filter_jobs_by_yoe(page, target_yoe):
    if target_yoe == "":
        return
    await page.wait_for_selector('#years:not([disabled])', state='visible', timeout=5000)
    await page.click('#years')
    await page.type('#years', target_yoe, delay=10)



async def filter_jobs_by_job_function(page, target_job_func_arr):
    if not target_job_func_arr:
        return
    job_func_selector = "div.selectize-control.ng-isolate-scope.ng-pristine.ng-valid.multi.plugin-remove_button"
    await page.locator(job_func_selector).nth(1).click()
    await page.wait_for_timeout(300)  # Wait for dropdown to open

    job_func_option_selector = "div.option.selectize-option.nested-option"

    target_job_func_arr = target_job_func_arr[:3] # Use only the first 3 job functions for selection
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




async def filter_jobs_by_location(page, target_location_arr):
    if not target_location_arr:
        return
    location_selector = "div.selectize-control.ng-isolate-scope.ng-pristine.ng-valid.multi.plugin-remove_button"
    await page.locator(location_selector).nth(3).click()
    await page.wait_for_timeout(300)

    location_option_selector = "div.selectize-dropdown-content div.option"

    target_location_arr = target_location_arr[:15] # Use only the first 15 locations for selection
    target_location_arr = [normalise_text(t) for t in target_location_arr]
    target_location_set = set(target_location_arr)

    for target_location in target_location_arr:
        # Re-open the dropdown before each selection
        await page.locator(location_selector).nth(3).click()
        await page.wait_for_timeout(300)
        options = await page.query_selector_all(location_option_selector)
        found = False
        for opt in options:
            text = await opt.inner_text()
            option_text = normalise_text(text)
            if option_text == target_location:
                try:
                    await opt.scroll_into_view_if_needed()
                    await opt.click()
                    print(f"Clicked '{text}' option.")
                    found = True
                    break
                except Exception as click_err:
                    print(f"Failed to click '{text}' option: {click_err}")
        if not found:
            print(f"Option matching '{target_location}' not found.")



async def filter_jobs_by_size(page, target_company_size):
    if target_company_size == "":
        return

    target_company_size = normalise_text(target_company_size)
    size_map = {
        'all': '0',
        'small': '1',
        'large': '2',
        'medium': '3',
    }
    value = size_map.get(target_company_size)
    if value is None:
        print(f"Unknown company size: {target_company_size}")
        return

    select_selector = '#company-size'
    await page.wait_for_selector(select_selector, timeout=3000)
    await page.select_option(select_selector, value=value)
    print(f"Selected company size: {target_company_size.title()}")



def normalise_text(text):
    return text.replace(' ', '').replace('-', '').lower()