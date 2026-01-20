from pydantic import BaseModel, EmailStr
from typing import List
class SignupRequest(BaseModel):
    name:str
    email: EmailStr
    password: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class AuthResponse(BaseModel):
    message: str
    acess_token: str | None=None
class CreateProjectRequest(BaseModel):
    doc_type:str
    topic:str
class SectionItem(BaseModel):
    title:str
    position:int
class SlideItem(BaseModel):
    title:str
    position:int
class WordConfigRequest(BaseModel):
    project_id:str
    sections:List[SectionItem]
class PPTConfigRequest(BaseModel):
    project_id:str
    slides:List[SlideItem]
