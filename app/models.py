from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # make sure this path matches your structure

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

    # Relationship to choices
    choices = relationship("Choice", back_populates="question", cascade="all, delete")

class Choice(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("questions.id"))

    # Back reference to question
    question = relationship("Question", back_populates="choices")
