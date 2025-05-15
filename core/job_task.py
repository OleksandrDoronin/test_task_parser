import os
import subprocess
import time


from datetime import datetime, timezone
import schedule

from core.logger import logger
from core.settings import settings


def create_dump():
    """Create a database dump with UTC timestamp."""
    dumps_folder = 'dumps'
    os.makedirs(dumps_folder, exist_ok=True)

    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S_UTC')
    dump_filename = f'{dumps_folder}/db_dump_{current_time}.sql'

    logger.info(f'Starting to create dump: {dump_filename}')
    command = (
        f'PGPASSWORD={settings.postgres_password} '
        f'pg_dump -U {settings.postgres_user} '
        f'-h {settings.postgres_host} '
        f'-d {settings.postgres_db} '
        f'-F c -b -v '
        f'-f {dump_filename}'
    )
    try:
        subprocess.run(command, shell=True, check=True)
        logger.info(f'Successfully created dump: {dump_filename}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error creating dump: {e}', exc_info=True)


def run_spider():
    """Launch Scrapy Spider."""
    logger.info('Starting the AutoRio spider...')
    try:
        subprocess.run(['scrapy', 'crawl', 'autoria_spider'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error when starting spider: {e}')


def schedule_daily_dump():
    """Schedule a daily dump at 12:00 UTC."""
    schedule.every().day.at('12:00').do(create_dump)


def schedule_spider():
    """Schedule spider run every 1 minute."""
    schedule.every(1).minute.do(run_spider)


def run_jobs():
    logger.info("Starting scheduled jobs...")
    schedule_daily_dump()
    schedule_spider()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")