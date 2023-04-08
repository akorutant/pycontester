import sqlalchemy

from .db_session import SqlAlchemyBase


class Contests(SqlAlchemyBase):
    __tablename__ = "contests"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)

