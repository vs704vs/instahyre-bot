from playwright.async_api import Page

async def apply_jobs(page: Page):
	# Wait for the button with id 'interested-btn' and inner text containing 'View'
	view_job_selector = "#interested-btn"
	await page.wait_for_selector(view_job_selector, timeout=5000)