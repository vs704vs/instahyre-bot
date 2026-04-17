from playwright.async_api import Page

async def apply_jobs(page: Page):
	# Wait for the button with id 'interested-btn' and inner text containing 'View'
	view_job_selector = "#interested-btn"
	await page.wait_for_selector(view_job_selector, timeout=5000)
	try:
		await page.locator(view_job_selector).nth(0).click()

		apply_selector = "button.btn.btn-lg.btn-primary.new-btn"
		while True:
			await page.locator(apply_selector).click()
			print("Clicked 'Apply' button.")
			await page.wait_for_timeout(2000)

		# Final click for 1 remaining job after loop, only if selector exists
		if await page.locator(apply_selector).count() > 0:
			await page.locator(apply_selector).click()
            
	except Exception as e:
		print(f"No button with id 'interested-btn' could be clicked: {e}")