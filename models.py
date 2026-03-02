from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    encrypted_data = Column(String)