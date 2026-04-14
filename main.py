import asyncio
from login import login_main, close_browser
from jobs import handle_jobs

async def orchestrate():
    page, browser = await login_main()
    if page is not None:
        await handle_jobs(page)
    await close_browser()

if __name__ == "__main__":
    asyncio.run(orchestrate())
