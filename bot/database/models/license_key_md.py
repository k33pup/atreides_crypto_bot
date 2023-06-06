from bot.database.base import Base
import sqlalchemy
from datetime import datetime


class LicenseKey(Base):
    __tablename__ = 'license_keys'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f"<LICENSE KEY> {self.id} {self.type} {self.key} {self.duration}"

