# from fastapi import FastAPI
# from app.routes import health

# app = FastAPI()

# app.include_router(health.healthRoute)


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session

from app import models
from app.database import engine, sessionLocal
from app.routes import health

# Create FastAPI instance
app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

# Dependency to get DB session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Routes
@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question is not found')
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choice).filter(models.Choice.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choice is not found')
    return result

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choice(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()

    return {"message": "Question created successfully"}
