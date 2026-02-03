from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class HustleBase(SQLModel):
    full_name: str
    email: str
    raw_experience: str

class HustleProfile(HustleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_id: str = Field(index=True, unique=True)
    formatted_cv: Optional[str] = None

class HustleRead(HustleBase):
    id: int
    formatted_cv: Optional[str]

sqlite_file_name = "hustle.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)