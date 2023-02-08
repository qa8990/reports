from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List
#models.Base.metadata.create_all(bind=engine)

api = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api.post("/api/v1/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@api.get("/api/v1/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users, "USERS #######")
    return users


@api.get("/api/v1/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@api.get("/api/v1/users-by/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email = user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@api.get("/api/v1/status/", response_model=List[schemas.Status])
def read_status(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    estatus = crud.get_status(db, skip=skip, limit=limit)
    return estatus

@api.get("/api/v1/companies/", response_model=List[schemas.Companies])
async def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    company = crud.get_companies(db, skip=skip, limit=limit)
    return company

@api.get("/api/v1/company/{companyId}", response_model=schemas.Companies)
def get_company_byId(companyId: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, companyId)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@api.get("/api/v1/last-company/", response_model=schemas.Companies)
async def read_last_company_added(db: Session = Depends(get_db)):
    last_company = crud.get_last_company_added(db)
    return last_company

@api.post("/api/v1/company/", response_model=schemas.CompanyCreate)
async def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db) ):
    print("datos de compania", company)
    return crud.add_company(db=db, company=company)

@api.put("/api/v1/company/{company_id}", response_model=schemas.CompanyCreate)
async def update_company(company_id: int, company: schemas.CompanyCreate,  db: Session = Depends(get_db)):
    db_company = crud.upd_company(db, company_id, company)
    print(type(db_company))
    print("Actualizando datos de compania", db_company)
    return db_company

@api.get("/api/v1/company-types/", response_model=List[schemas.CompanyTypes])
def read_companytypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companyType = crud.get_company_types(db, skip=skip, limit=limit)
    print(companyType, "COMPANY TYPE")
    return companyType