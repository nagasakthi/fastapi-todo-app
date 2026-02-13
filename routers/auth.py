from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException ,Request
from pydantic.v1 import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_Context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = "d645975dbe3012580c115daa0147a85ffad31dbf4fd26974e45f52216f3734af"
ALGORITHM = "HS256"

class CreateUserRequest(BaseModel):
    email : str
    password : str
    username : str
    firstname : str
    lastname : str
    role : str

# Dependency for DB session:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates")

#### PAGES ####
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#### END POINTS   ####

def authenticate_user(username : str,password : str,db ): # Helper function
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_Context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username : str,user_id : str, role : str, expires_delta: timedelta ):
    encode = {
        'sub' : username,
        'id' : user_id,
        'role': role
    }
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp' : expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return {'username': username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user: CreateUserRequest):
    # create_user = User(**create_user.dict())
    create_user = User(
        email=create_user.email,
        hashed_password=bcrypt_Context.hash(create_user.password),
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        role=create_user.role,
        is_active=True
    )
    db.add(create_user)
    db.commit()

@router.get("/")
async def read_all(db: db_dependency):
    users = db.query(User).all()
    return users

@router.post("/token",status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated [OAuth2PasswordRequestForm ,Depends()], db: db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=30))
    # return token
    return {"access_token": token,"token_type": "bearer"}


@router.delete("/delete",status_code=status.HTTP_200_OK)
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "Deleted successfully",'Delete user': user}



