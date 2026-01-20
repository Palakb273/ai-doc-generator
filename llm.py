import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
def generate_text(prompt:str)->str:
    response=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"system","content":"You are a professional business document writer."},{"role":"user","content":prompt}],
    temperature=0.3,
    max_tokens=400)
    return response.choices[0].message.content