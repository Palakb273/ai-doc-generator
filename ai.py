from fastapi import APIRouter, HTTPException, Header
from database import supabase
from llm import generate_text
from config import get_user_from_token
from pydantic import BaseModel
router=APIRouter(prefix="/ai",tags=["AI"])
@router.post("/generate/{project_id}")
def generate_content(project_id: str):
    sections=supabase.table("sections") \
        .select("*") \
        .eq("project_id",project_id) \
        .execute()
    if not sections.data:
        raise HTTPException(status_code=404,detail="Sections not found")
    results=[]
    for section in sections.data:
        prompt=f"""Write a professional, well-structured section for a word document.
        Section Title:{section['title']}
        Tone:Formal, clear and Business-like
        Length: 150-200 words
        Use proper paragraphs and smooth flow.
        """
        try:
            content=generate_text(prompt)
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"Groq error:{str(e)}")
        supabase.table("ai_generations").insert({"project_id":project_id,"section_id":section['id'],"content":content}).execute()
        results.append({"section_id":section['id'],"title":section['title'],"content":content})
    return{"message":"AI Generation completed","generated_sections":results}
@router.get("/content/{project_id}")
def get_ai_content(project_id: str):
    data=supabase.table("ai_generations") \
        .select("*, sections(title)") \
        .eq("project_id",project_id) \
        .execute()
    return{"content":data.data}
class RefineRequest(BaseModel):
    project_id: str
    section_id:str
    refined_text:str
@router.post("/save-refinement")
def save_refinement(payload:RefineRequest):
    supabase.table("refined_content").upsert({"project_id":payload.project_id,"section_id":payload.section_id,"refined_text":payload.refined_text}).execute()
    return{"message":"Refinement saved successfully"}
