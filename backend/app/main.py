from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from .models import create_db_and_tables, engine, HustleProfile, HustleBase
from .ai_service import transform_hustle_to_cv

app = FastAPI(title="Hustle-to-CV API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        
        if "Error" in professional_cv:
            raise HTTPException(status_code=500, detail="AI transformation failed")

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
                clerk_id="pending_auth"
            )
            session.add(new_profile)
        
        session.commit()
        return {"status": "success", "cv": professional_cv}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))