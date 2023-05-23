import sqlalchemy
from sqlalchemy.util.preloaded import orm

from .db_session import SqlAlchemyBase


class ContestResults(SqlAlchemyBase):
		__tablename__ = "contests_results"

		id = sqlalchemy.Column(sqlalchemy.Integer,
							primary_key=True, autoincrement=True)

		student_id = sqlalchemy.Column(sqlalchemy.Integer,
									sqlalchemy.ForeignKey("users.id"))
		contest_id = sqlalchemy.Column(sqlalchemy.Integer,
									sqlalchemy.ForeignKey("contests.id"))
		complited = sqlalchemy.Column(sqlalchemy.Integer)
		count_tasks = sqlalchemy.Column(sqlalchemy.Integer)
		student = orm.relationship("User")