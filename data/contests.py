import datetime as dt
import sqlalchemy
from sqlalchemy.util.preloaded import orm

from .db_session import SqlAlchemyBase


contest_to_task_table = sqlalchemy.Table(
    'contest_to_task',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('contest', sqlalchemy.Integer, sqlalchemy.ForeignKey('contests.id')),
    sqlalchemy.Column('task', sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id'))
)


class Contest(SqlAlchemyBase):
    __tablename__ = "contests"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("teachers.user_id"))
    join_deadline = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    end_deadline = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    teacher = orm.relationship('Teacher')
    tasks = orm.relationship('Task', secondary='contest_to_task', backref='contest')