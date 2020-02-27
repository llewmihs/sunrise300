from crontab import CronTab
my_cron = CronTab(user='pi')

for job in my_cron:
    print(job)

job = my_cron.new(command='python3 /home/pi/justpics.py')

job.setall(time(10,2))