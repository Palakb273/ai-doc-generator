from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from auth import router as auth_router
from config import router as config_router
from ai import router as ai_router
from export import router as export_router
import os
load_dotenv()

app=FastAPI(title="AI Document Generator API")
origins=["https://ai-doc-generator-frontend.vercel.app","https://ai-doc-generator-frontend-n2q7ehvq4-palak-bishts-projects.vercel.app"]

            
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(config_router)
app.include_router(ai_router)
app.include_router(export_router)
@app.get("/")
def root():
    return{"message":"Backend is running successfully"}
