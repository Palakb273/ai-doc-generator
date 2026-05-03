from fastapi import APIRouter, HTTPException, Header
from database import supabase
from llm import generate_text
from config import get_user_from_token
from pydantic import BaseModel
router=APIRouter(prefix="/ai",tags=["AI"])

def get_project_topic(project_id: str) -> str:
    """Fetch the topic for a project from the projects table."""
    project = supabase.table("projects") \
        .select("topic, doc_type") \
        .eq("id", project_id) \
        .execute()
    if not project.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.data[0].get("topic", ""), project.data[0].get("doc_type", "docx")

@router.post("/generate/{project_id}")
def generate_content(project_id: str):
    topic, doc_type = get_project_topic(project_id)

    sections = supabase.table("sections") \
        .select("*") \
        .eq("project_id", project_id) \
        .order("position") \
        .execute()

    if not sections.data:
        sections = supabase.table("slides") \
            .select("*") \
            .eq("project_id", project_id) \
            .order("position") \
            .execute()

    if not sections.data:
        raise HTTPException(status_code=404, detail="No sections or slides found for this project")

    supabase.table("ai_generations") \
        .delete() \
        .eq("project_id", project_id) \
        .execute()

    results = []
    total_sections = len(sections.data)

    for idx, section in enumerate(sections.data, start=1):
        if doc_type == "pptx":
            prompt = f"""You are writing content for a PowerPoint presentation about: {topic}
This is slide {idx} of {total_sections}.
Slide Title: {section['title']}

Write 4-6 concise bullet points for this slide. Each bullet point should be:
- Directly related to the topic {topic}
- Specific to the slide title {section['title']}
- Clear, informative, and presentation-ready
- Between 10-25 words each

Do NOT write generic content. The content must be factual and specific to {topic} under the aspect of {section['title']}.
Only output the bullet points, no extra text."""
        else:
            prompt = f"""You are writing a section for a professional document about: {topic}

This is section {idx} of {total_sections}.
Section Title: {section['title']}

Write a detailed, well-structured section (150-250 words) that:
- Is specifically about {topic} as it relates to {section['title']}
- Contains factual, relevant information specific to this topic
- Uses a formal, clear, and professional tone
- Has proper paragraphs with smooth flow
- Does NOT contain generic filler — every sentence must relate to {topic}

Do NOT repeat the section title. Jump straight into the content."""

        try:
            content = generate_text(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Groq error: {str(e)}")

        # ── THIS IS THE FIX ───────────────────────────────────────────
        if doc_type == "pptx":
            supabase.table("ai_generations").insert({
                "project_id": project_id,
                "slide_id": section['id'],    # slides table id
                "content": content
            }).execute()
        else:
            supabase.table("ai_generations").insert({
                "project_id": project_id,
                "section_id": section['id'],  # sections table id
                "content": content
            }).execute()
        # ─────────────────────────────────────────────────────────────

        results.append({
            "section_id": section['id'],
            "title": section['title'],
            "content": content
        })

    return {"message": "AI Generation completed", "generated_sections": results}


@router.get("/content/{project_id}")
def get_ai_content(project_id: str):
    data = supabase.table("ai_generations") \
        .select("*, sections(title)") \
        .eq("project_id", project_id) \
        .execute()

    if not data.data:
        data = supabase.table("ai_generations") \
            .select("*, slides(title)") \
            .eq("project_id", project_id) \
            .execute()

    return {"content": data.data}


class RefineRequest(BaseModel):
    project_id: str
    section_id: str
    refined_text: str

@router.post("/save-refinement")
def save_refinement(payload: RefineRequest):
    supabase.table("refined_content").upsert({
        "project_id": payload.project_id,
        "section_id": payload.section_id,
        "refined_text": payload.refined_text
    }).execute()
    return {"message": "Refinement saved successfully"}
