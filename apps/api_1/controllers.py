from .. import db
from ..models import OpsResult, OpsEvent


class OpsResultHandler(object):
    @staticmethod
    def list(task_id):
        tasks = OpsResult.query.filter(OpsResult.log_id == task_id).all()
        return tasks

    @staticmethod
    def listall():
        tasks = db.session.query(OpsResult).all()
        return tasks

    @staticmethod
    def create(kw):
        try:
            result = OpsResult(**kw)
            db.session.add(result)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}

    @staticmethod
    def update(task_id, kw):
        try:
            db.session.query(OpsResult).filter(OpsResult.log_id == task_id).update(kw)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}

    @staticmethod
    def delete(task_id):
        try:
            to_delete = OpsResult.query.filter(OpsResult.log_id == task_id).first()
            db.session.delete(to_delete)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}


class OpsEventHandler(object):
    @staticmethod
    def list(task_id):
        tasks = OpsEvent.query.filter(OpsEvent.log_id == task_id).all()
        return tasks

    @staticmethod
    def listall():
        tasks = db.session.query(OpsEvent).all()
        return tasks

    @staticmethod
    def create(kw):
        try:
            result = OpsEvent(**kw)
            db.session.add(result)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}

    @staticmethod
    def update(task_id, kw):
        try:
            db.session.query(OpsEvent).filter(OpsEvent.log_id == task_id).update(kw)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}

    @staticmethod
    def delete(task_id):
        try:
            to_delete = OpsEvent.query.filter(OpsEvent.log_id == task_id).first()
            db.session.delete(to_delete)
            db.session.commit()
            return {'flag': True, 'message': ''}
        except Exception as e:
            return {'flag': False, 'message': str(e)}
