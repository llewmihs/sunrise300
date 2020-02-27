from crontab import CronTab
my_cron = CronTab(user='pi')

for job in my_cron:
    print(job)

job = my_cron.new(command='python3 /home/pi/justpics.py')

job.hour.on(2)
job.minute.on(10)

my_cron.write()