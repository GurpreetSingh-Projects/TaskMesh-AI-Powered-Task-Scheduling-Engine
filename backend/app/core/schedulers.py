from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler= AsyncIOScheduler(timezone= "Asia/Kolkata")

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def end_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
