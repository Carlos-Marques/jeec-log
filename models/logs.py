from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    
    user_id = Column(String(20))
    entrypoint = Column(String(200), nullable=False)
    create_date = Column(DateTime, server_default=func.now())