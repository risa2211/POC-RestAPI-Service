from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone, date

from models import UserCreate, UserProfile, Sport, SportStat
from data import MOCK_USER_DB, SPORTS_DATA

app = FastAPI(title="POC RestAPI")

# I'll be using a minimal JWT Configuration since this is a POC 
SECRET_KEY = "secret-key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data = MOCK_USER_DB.get(user_email)
    if user_data is None:
        raise credentials_exception
    
    return UserProfile(**user_data['profile_data'])

@app.post("/signup")
async def signup(user: UserCreate):
    if user.email in MOCK_USER_DB:
        raise HTTPException(status_code=400, detail="Email has been already registered")
    profile_data = user.model_dump(exclude={"password"})

    # To Calculate AGE 
    today = date.today()
    user_dob: date = user.dob 
    age = today.year - user_dob.year - ((today.month, today.day) < (user_dob.month, user_dob.day))
    profile_data['age'] = age 
    MOCK_USER_DB[user.email] = {
        "password_hash": user.password,
        "profile_data": profile_data, 
    }
    return {"message": "User is registered successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()): 
    user_entry = MOCK_USER_DB.get(form_data.username)    
    if not user_entry or user_entry['password_hash'] != form_data.password: 
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile", response_model=UserProfile)
async def get_profile(current_user: UserProfile = Depends(get_current_user)):
    return current_user

@app.put("/profile")
async def update_profile(
    updated_data: UserCreate, 
    current_user: UserProfile = Depends(get_current_user)
):
    # Excluded password so that it is not exposed as a general security practice
    profile_data = updated_data.model_dump(exclude={"password"})

    # if updating the date in profile, recalculate the age, found this while testing that it was picking the older age itself
    today = date.today()
    user_dob: date = updated_data.dob 
    age = today.year - user_dob.year - ((today.month, today.day) < (user_dob.month, user_dob.day))
    profile_data['age'] = age 
    MOCK_USER_DB[current_user.email]["profile_data"] = profile_data
    return {"message": "Profile updated successfully"}

@app.get("/sports", response_model=list[Sport])
async def get_sports_list():
    return SPORTS_DATA

@app.get("/sports/{sport_name}", response_model=Sport)
async def get_sport_stats(sport_name: str):
    sport_data = None

    for s in SPORTS_DATA:
        if s["name"].lower() == sport_name.lower():
            sport_data = s   
    if not sport_data:
        raise HTTPException(status_code=404, detail="Sport not found")
    return Sport(**sport_data)

@app.get("/health")
async def health_check():
    return {"message": "POC API is running!"}
