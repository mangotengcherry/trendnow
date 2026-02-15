from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from database import get_db
from models import User
import schemas
import auth_utils
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Replace with your actual Google Client ID
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_PLACEHOLDER" 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth_utils.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/google", response_model=schemas.Token)
async def google_login(login_data: schemas.GoogleLogin, db: Session = Depends(get_db)):
    try:
        # Verify Google Token
        # Note: In a real app, you MUST uncomment and use the verification.
        # idinfo = id_token.verify_oauth2_token(login_data.token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        # For this demo/development, since we don't have a real client ID setup in frontend yet,
        # we will simulate verification by decoding the token safely if possible, or just trusting the mock.
        # If the frontend sends a mock token, we'll accept it.
        
        if login_data.token.startswith("mock_token_"):
            # Simulation for development
            email = login_data.token.replace("mock_token_", "") + "@example.com"
            google_id = "mock_" + login_data.token
            name = "Mock User " + login_data.token
        else:
            # Real verification logic
            idinfo = id_token.verify_oauth2_token(login_data.token, google_requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo['email']
            google_id = idinfo['sub']
            name = idinfo.get('name')

        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Create new user
            user = User(
                email=email,
                google_id=google_id,
                full_name=name,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update google_id if missing (linking account)
            if not user.google_id:
                user.google_id = google_id
                db.commit()

        # Create JWT
        access_token_expires = auth_utils.timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_utils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
            "has_password": user.hashed_password is not None
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")

@router.post("/login", response_model=schemas.Token)
async def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not auth_utils.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = auth_utils.create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "has_password": True
    }

@router.post("/password")
async def set_password(
    password_data: schemas.PasswordSet, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    hashed_password = auth_utils.get_password_hash(password_data.password)
    current_user.hashed_password = hashed_password
    db.commit()
    return {"message": "Password set successfully"}
