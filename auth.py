from sqlalchemy.orm import Session
from uuid import uuid4
from modelclass import UserDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sessions = {}

def authenticate_user(db: Session, identifier: str, password: str):
    user = db.query(UserDB).filter(
        (UserDB.Username == identifier) | (UserDB.Email == identifier)
    ).first()
    if user and pwd_context.verify(password, user.Password):
        return user
    return None

def create_session(user):
    session_id = str(uuid4())
    sessions[session_id] = user
    return session_id
