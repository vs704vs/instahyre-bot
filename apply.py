from playwright.async_api import Page

async def apply_jobs(page: Page):
	# Wait for the button with id 'interested-btn' and inner text containing 'View'
	view_job_selector = "#interested-btn"
	await page.wait_for_selector(view_job_selector, timeout=5000)
	try:
		await page.locator(view_job_selector).nth(0).click()
		await page.wait_for_timeout(1000)

		apply_selector = "button.btn.btn-lg.btn-primary.new-btn"
		apply_count = 0
		
		while await page.locator(apply_selector).count() > 0:
			await page.locator(apply_selector).click()
			apply_count += 1
			await page.wait_for_timeout(1500)

		await page.locator(view_job_selector).nth(0).click()
		await page.locator(apply_selector).click()
		apply_count += 1

		print(f"Applied to {apply_count} job(s).")

	except Exception as e:
		print(f"No button with id 'interested-btn' could be clicked: {e}")