from crontab import CronTab
my_cron = CronTab(user='pi')

for job in my_cron:
    print(job)