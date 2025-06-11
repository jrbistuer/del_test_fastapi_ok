from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class Usuaris(Base):
    __tablename__ = 'usuaris'

    US_Id = Column(Integer, primary_key=True, autoincrement=True)
    US_Nom = Column(String(100), nullable=False)
    US_Cognoms = Column(String(120), nullable=False)
    US_Email = Column(String(100), nullable=False)
    US_Status = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Usuaris(nom={self.US_Nom}, cognoms={self.US_Cognoms}, email={self.US_Email}, status={self.US_Status})>"
    