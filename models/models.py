from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class Usuaris(Base):
    __tablename__ = 'usuaris'

    US_Id = Column(Integer, primary_key=True, autoincrement=True)
    US_Id_Session = Column(String(100), nullable=False)
    US_Nom = Column(String(100), nullable=False)
    US_Cognoms = Column(String(120), nullable=False)
    US_Email = Column(String(100), nullable=False)
    US_Status = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Usuaris(nom={self.US_Nom}, cognoms={self.US_Cognoms}, email={self.US_Email}, status={self.US_Status})>"
    
class Pedidos(Base):
    __tablename__ = 'pedidos'

    PED_Id = Column(Integer, primary_key=True, autoincrement=True)
    PED_Id_User = Column(String(100), nullable=False)
    PED_Nombre = Column(String(100), nullable=False)
    PED_Descripcion = Column(String(255), nullable=True)
    PED_Precio = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Pedidos(id={self.PED_Id}, user_id={self.PED_Id_User}, nombre={self.PED_Nombre}, descripcion={self.PED_Descripcion}, precio={self.PED_Precio})>"

