import traceback
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .models import create_db_and_tables, engine, HustleProfile, HustleBase
from .ai_service import transform_hustle_to_cv

app = FastAPI(title="Hustle-to-CV API")

# Senior Tip: Explicitly allow the Authorization header for Clerk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all to rule out CORS as the culprit
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
        # 1. AI Call (Using the free model logic in ai_service.py)
        professional_cv = transform_hustle_to_cv(data.raw_experience)
        
        if "Error" in professional_cv:
            # If AI fails, we still return a 200 with the error message so the 
            # Frontend can show the user what happened instead of just crashing.
            return {"status": "partial_success", "cv": f"AI was unavailable, but your data is saved. Error: {professional_cv}"}

        # 2. Database logic
        statement = select(HustleProfile).where(HustleProfile.email == data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            existing_user.raw_experience = data.raw_experience
            existing_user.formatted_cv = professional_cv
            session.add(existing_user)
        else:
            new_profile = HustleProfile(
                full_name=data.full_name,
                email=data.email,
                raw_experience=data.raw_experience,
                formatted_cv=professional_cv,
                clerk_id=f"guest_{data.email}" 
            )
            session.add(new_profile)
        
        session.commit()
        return {"status": "success", "cv": professional_cv}
        
    except Exception as e:
        print("\n" + "="*60)
        traceback.print_exc() 
        print("="*60 + "\n")
        raise HTTPException(status_code=500, detail=str(e))