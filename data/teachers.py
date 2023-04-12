import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
