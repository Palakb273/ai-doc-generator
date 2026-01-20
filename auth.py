from fastapi import APIRouter, HTTPException
from database import supabase
from schemas import SignupRequest, LoginRequest
router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/signup")
def signup(data:SignupRequest):
    try:
        response=supabase.auth.sign_up({
            "email":data.email,
            "password": data.password,
            "options":{
                "data":{"name":data.name}
            }
        })
        if not response.user:
            raise HTTPException(status_code=400,detail="signup failed")
        return{
            "message":"User registered successfully",
            "access_token":response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
@router.post("/login")
def login(data:LoginRequest):
    try:
        response=supabase.auth.sign_in_with_password({
            "email":data.email,
            "password": data.password,
        })
        if not response.user:
            raise HTTPException(status_code=400,detail="invalid credentials")
        return{
            "message":"User logged in successfully",
            "access_token":response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=401,detail=str(e))