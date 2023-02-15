from fastapi import Depends, FastAPI, HTTPException
from fastapi_pagination import Page, paginate, LimitOffsetPage, add_pagination, Params
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List


api = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api.get("/api/v1/status/", response_model=List[schemas.Status], tags=["Status"])
def read_status(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    estatus = crud.get_status(db, skip=skip, limit=limit)
    return estatus

@api.post("/api/v1/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@api.get("/api/v1/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users, "USERS #######")
    return users


@api.get("/api/v1/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@api.get("/api/v1/users-by/{user_email}", response_model=schemas.User, tags=["Users"])
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email = user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@api.get("/api/v1/company-types/", response_model=List[schemas.CompanyTypes], tags=["Company Types"])
def read_companytypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companyType = crud.get_company_types(db, skip=skip, limit=limit)
    print(companyType, "COMPANY TYPE")
    return companyType

@api.get("/api/v1/last-company/", response_model=schemas.Companies, tags=["Companies"])
async def read_last_company_added(db: Session = Depends(get_db)):
    last_company = crud.get_last_company_added(db)
    #print("LAST COMPANY", last_company)
    return last_company

@api.get("/api/v1/companies/", response_model=List[schemas.Companies], tags=["Companies"])
async def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    company = crud.get_companies(db, skip=skip, limit=limit)
    return company

@api.get("/api/v1/company/{companyId}/", response_model=schemas.Companies, tags=["Companies"])
def get_company_byId(companyId: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, companyId)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@api.post("/api/v1/company/", response_model=schemas.CompanyCreate, tags=["Companies"])
async def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db) ):
    print(" Estoy en el POST v1/company")
    print("Creando datos de compania", company)
    return crud.add_company(db=db, company=company)

@api.put("/api/v1/company/{company_id}/", response_model=schemas.CompanyCreate, tags=["Companies"])
async def update_company(company_id: int, company: schemas.CompanyCreate,  db: Session = Depends(get_db)):
    db_company = crud.upd_company(db, company_id, company)
    print(" Estoy en el PUT v1/company")
    print(type(db_company))
    print("Actualizando datos de compania", db_company)
    return db_company

@api.get("/api/v1/masterplans/", response_model=Page[schemas.MasterPlan], tags=["Master Plan"])
async def read_masterplan(skip: int , limit: int = 20, db: Session = Depends(get_db)):
    print(" AJA Y ANDEN ???? what")
    params = Params(size=limit, page=skip)
    accounts = crud.get_master_plan(db, skip=skip, limit=limit)
    print(accounts, "MASTER PLAN")
    print(type(accounts))
    return paginate(accounts, params)