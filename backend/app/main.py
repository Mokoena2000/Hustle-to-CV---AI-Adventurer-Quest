import traceback
import io
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from reportlab.pdfgen import canvas

from .models import create_db_and_tables, engine, HustleProfile, HustleBase
from .ai_service import transform_hustle_to_cv

app = FastAPI(title="Hustle-to-CV API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hustle-to-CV API is running"}

@app.post("/generate")
async def generate_cv(data: HustleBase, session: Session = Depends(get_session)):
    try:
        professional_cv = transform_hustle_to_cv(data.raw_experience)
        
        # Check if the AI returned a real result or an error string
        is_ai_error = "AI Error" in professional_cv
        
        statement = select(HustleProfile).where(HustleProfile.email == data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            existing_user.raw_experience = data.raw_experience
            # Only update CV if AI actually worked
            if not is_ai_error:
                existing_user.formatted_cv = professional_cv
            session.add(existing_user)
        else:
            new_profile = HustleProfile(
                full_name=data.full_name,
                email=data.email,
                raw_experience=data.raw_experience,
                formatted_cv=None if is_ai_error else professional_cv,
                clerk_id=f"guest_{data.email}" 
            )
            session.add(new_profile)
        
        session.commit()

        if is_ai_error:
            return {"status": "partial_success", "cv": f"Saved, but AI failed: {professional_cv}"}
        
        return {"status": "success", "cv": professional_cv}
        
    except Exception as e:
        print("\n" + "="*60)
        traceback.print_exc() 
        print("="*60 + "\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-cv/{email}")
async def download_cv(email: str, session: Session = Depends(get_session)):
    """Generates a PDF on the fly for the user."""
    statement = select(HustleProfile).where(HustleProfile.email == email)
    user_profile = session.exec(statement).first()
    
    if not user_profile or not user_profile.formatted_cv:
        raise HTTPException(status_code=404, detail="CV not found or not generated yet")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # PDF Styling
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 800, f"Professional Experience: {user_profile.full_name}")
    
    p.setFont("Helvetica", 12)
    text_object = p.beginText(100, 760)
    for line in user_profile.formatted_cv.split('\n'):
        text_object.textLine(line)
    p.drawText(text_object)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(), 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename={user_profile.full_name}_CV.pdf"}
    )