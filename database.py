from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    predictions = relationship("Prediction", back_populates="user")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symptoms = Column(JSON)  # Store symptoms as JSON array
    severity = Column(Integer)
    predicted_disease = Column(String)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="predictions")
    recommendations = relationship("Recommendation", back_populates="prediction")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    herbs = Column(JSON)  # Store herbs as JSON array
    lifestyle = Column(JSON)  # Store lifestyle recommendations as JSON array
    diet = Column(JSON)  # Store diet recommendations as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    
    prediction = relationship("Prediction", back_populates="recommendations")

# Create database tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_prediction(db, age, gender, symptoms, severity, predicted_disease, confidence_score, recommendations):
    """Save prediction and recommendations to database"""
    # Create new user
    user = User(age=age, gender=gender)
    db.add(user)
    db.flush()
    
    # Create prediction
    prediction = Prediction(
        user_id=user.id,
        symptoms=symptoms,
        severity=severity,
        predicted_disease=predicted_disease,
        confidence_score=confidence_score
    )
    db.add(prediction)
    db.flush()
    
    # Create recommendation
    recommendation = Recommendation(
        prediction_id=prediction.id,
        herbs=recommendations['herbs'],
        lifestyle=recommendations['lifestyle'],
        diet=recommendations['diet']
    )
    db.add(recommendation)
    
    # Commit all changes
    db.commit()
    return prediction.id
  