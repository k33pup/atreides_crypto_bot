from bot.database.base import Base
import sqlalchemy
from datetime import datetime


class License(Base):
    __tablename__ = 'users_licenses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    expire_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    def __repr__(self):
        return f"<SUBSCRIPTION> {self.id} {self.user_id} {self.type} {self.expire_date}"

