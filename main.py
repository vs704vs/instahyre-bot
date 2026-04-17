import asyncio
from login import login_main, close_browser
from jobs import handle_jobs
from apply import apply_jobs
import time

async def orchestrate():
    page, browser = await login_main()
    if page is not None:
        await handle_jobs(page)
        await apply_jobs(page)
        time.sleep(5)  # Wait for any final actions to complete before closing the browser
    await close_browser()

if __name__ == "__main__":
    asyncio.run(orchestrate())
