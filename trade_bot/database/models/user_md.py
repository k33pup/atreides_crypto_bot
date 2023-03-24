from trade_bot.database.base import Base
import sqlalchemy
from datetime import datetime


class User(Base):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    license = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    binance_api_key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    binance_secret_api_key = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    join_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<USER> {self.id} {self.tg_id} {self.license} {self.join_date}"
