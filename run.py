from apps import create_app, db, scheduler
from apps.models import User, OpsItem, OpsInfo, OpsResult, CheckHistory, CheckHost, Host, ChenkJobs
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from apps.check.exts import add_job_scheduler

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 添加初始化定时例检任务
with app.app_context():
    init_jobs = db.session.query(ChenkJobs).filter(ChenkJobs.status == 1).all()
    for job in init_jobs:
        args = (job.content,)
        add_job_scheduler(scheduler, job_id=job.id, job_cron=job.cron_time, args=args)
scheduler.start()

if __name__ == '__main__':
    app.run()
