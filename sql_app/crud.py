from sqlalchemy.orm import Session
from sqlalchemy import func, select, update

from . import models, schemas


def get_user(db: Session, user_id: int):
    print("el email es ", user_id)
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
#    print("email :", user_email)
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_status(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Status).offset(skip).limit(limit).all()

# -- Companies --
# Get all companies
def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Companies).offset(skip).limit(limit).all()

# Get company by id
def get_company(db: Session, company_id: int):
    print("El company id es ", company_id)
    db_company = db.query(models.Companies).filter(models.Companies.company_id == company_id).first()
    return db_company

# Get company by code
def get_company_by_code(db: Session, code: str):
    #    print("email :", user_email)
    return db.query(models.Companies).filter(models.Companies.code == code).first()

def get_last_company_added(db: Session):
    max_date = db.query(func.max(models.Companies.created_at)).scalar()
    #last_company_added = models.Companies.query.filter_by(created_at = max_date).first()
    return db.query(models.Companies).filter(models.Companies.created_at == max_date).first()

def add_company(db: Session, company: schemas.CompanyCreate):
    company_data = models.Companies(company_id = company.company_id, name = company.name, description = company.description, code = company.code, company_type_id = company.company_type_id)
    db.add(company_data)
    db.commit()
    return company_data

def upd_company(db: Session, company_id: int, company: schemas.CompanyCreate):
    print("en el upd-company-data", company_id)
    company_data = get_company(db, company_id)
    company_data.name = company.name
    company_data.description = company.description
    company_data.code = company.code
    company_data.created_at = company_data.created_at
    company_data.status_id = company_data.status_id
    print(company_data)
    print("compnay data --> desde el endpoont" ,company)
    db.add(company_data)
    db.commit()

    return company_data

# Company types
# Get Company types
def get_company_types(db: Session, skip: int = 0, limit: int = 100):
    tipos = db.query(models.CompanyTypes).offset(skip).limit(limit).all()
    print("tipo", tipos)
    print("tipo detalles", tipos[0].code)
    return tipos

def get_company_type(db: Session, company_type_id: int):
    print("el email es ", company_type_id)
    return db.query(models.CompanyTypes).filter(models.CompanyTypes.company_type_id == company_type_id).first()

