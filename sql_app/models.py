from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from enum import Enum

from .database import Base

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String (1), unique = True, index = True)
    description = Column( String (64))
    bg_image = Column(String(200))

    usuario = relationship("User", back_populates="estatus")
    estatus_2 = relationship("Companies", back_populates="company_estatus")
    estatus_3 = relationship("MasterPlan", back_populates="account_estatus")

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String (64) )
    email = Column(String (64), unique=True, index=True)
    password = Column(String)
    status = Column(Integer, ForeignKey("status.id"))

    estatus = relationship("Status", back_populates="usuario")
    
class Companies(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True)
    name = Column(String(60))
    description = Column(String(200))
    code = Column(Integer, unique=True)
    company_type_id = Column(Integer, ForeignKey("company_types.company_type_id"))
    created_at = Column(String(20))
    status_id = Column(Integer,  ForeignKey("status.id"))

    company_estatus = relationship("Status", back_populates="estatus_2")
    company_type = relationship("CompanyTypes", back_populates="type")

class CompanyTypes(Base):
    __tablename__ = "company_types"

    company_type_id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    description = Column(String(200))
    status_id = Column(Integer,  ForeignKey("status.id"))   
    image = Column(String)


    type = relationship("Companies", back_populates="company_type")


class MasterPlan(Base):
    __tablename__ = "master_plan"

    id = Column(Integer, primary_key=True)
    account_number = Column(String(30), unique=True)
    account_name = Column(String(240))
    status_id = Column(Integer, ForeignKey("status.id"))

    account_estatus = relationship("Status", back_populates="estatus_3")

