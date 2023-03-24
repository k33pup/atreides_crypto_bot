from trade_bot.database.base import Base
import sqlalchemy
from datetime import datetime


class GeneralSetting(Base):
    __tablename__ = 'GeneralSettings'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    work_condition = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    strategy_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f"<USER> {self.user_id} {self.work_condition} {self.strategy_type}"


class OrderSettings(Base):
    __tablename__ = 'OrdersSettings'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    work_condition = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    strategy_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f"<USER> {self.user_id} {self.work_condition} {self.strategy_type}"
