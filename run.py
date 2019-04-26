from apps import create_app, db
from apps.models import User, OpsItem, OpsInfoVss, OpsInfoCl, OpsInfoIms, OpsInfoSec, OpsInfoVpmn
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run()
