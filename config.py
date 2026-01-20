from fastapi import APIRouter, HTTPException, Depends,Header
from supabase import Client
from database import supabase
from schemas import CreateProjectRequest, WordConfigRequest, PPTConfigRequest
router=APIRouter(prefix="/config",tags=["Configuration"])
def get_user_from_token(authorization:str | None):
    if not authorization:
        raise HTTPException(status_code=401,detail="missing authorization header")
    parts=authorization.split()
    if len(parts)!=2 or parts[0]!="Bearer":
        raise HTTPException(status_code=401,detail="invalid authorization format")
    token=parts[1]
    try:
        user=supabase.auth.get_user(token)
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401,detail="invalid or expired token")
@router.post("/create-project")
def create_project(data:CreateProjectRequest, authorization: str | None = Header(None)):
    user=get_user_from_token(authorization)
    project=supabase.table("projects").insert({
        "user_id":user.id,
        "doc_type":data.doc_type,
        "topic":data.topic
    }).execute()
    return {"project_id":project.data[0]["id"],"message":"Project created successfully"}
@router.post("/save-word-outline")
def save_word_outline(data:WordConfigRequest):
    supabase.table("sections") \
        .delete() \
        .eq("project_id",data.project_id) \
        .execute()
    rows=[{"project_id":data.project_id,"title":s.title,"position":s.position} for s in data.sections]
    supabase.table("sections").insert(rows).execute()
    return {"message":"Word outline saved successfully"}
@router.post("/save-ppt-slides")
def save_ppt_slides(data:PPTConfigRequest):
    supabase.table("slides") \
        .delete() \
        .eq("project_id",data.project_id) \
        .execute()
    rows=[{"project_id":data.project_id,"title":s.title,"position":s.position} for s in data.slides]
    supabase.table("slides").insert(rows).execute()
    return {"message":"PPT slides saved successfully"}