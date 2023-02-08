from typing import List, Union

from pydantic import BaseModel


class StatusBase(BaseModel):
    code: str
    description: Union[str, None] = None
    bg_image: str


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    #status: int
    estatus: Union[Status, None] = None

    class Config:
        orm_mode = True

class CompanyTypeBase(BaseModel):
    company_type_id: int

class CompanyTypes(CompanyTypeBase):
    code: str
    description: str
    image: str

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    company_id: int
    name: str
    description: str
    company_type_id: int

class CompanyCreate(CompanyBase):
    code: str

    class Config:
        orm_mode = True

class Companies(CompanyBase):
    code: str
    name: str
    description: str
    created_at: str
    company_estatus: Union[Status, None] = None
    company_type: Union[CompanyTypes, None] = None
  
    class Config:
        orm_mode = True


    