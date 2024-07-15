from fastapi import FastAPI, Depends, HTTPException

from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

ALGORITHM : str = "HS256"
SECRET_KEY : str = "A Secure Secret Key"



def create_access_token(subject: str , expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt


app = FastAPI()

fake_users_db: dict[str, dict[str, str]] = {
    "ameenalam": {
        "username": "ameenalam",
        "full_name": "Ameen Alam",
        "email": "ameenalam@example.com",
        "password": "ameenalamsecret",
    },
    "mjunaid": {
        "username": "mjunaid",
        "full_name": "Muhammad Junaid",
        "email": "mjunaid@example.com",
        "password": "mjunaidsecret",
    },
    "masifansari": {
        "username": "masifansari",
        "full_name": "Asif Ansari",
        "email": "masifansari@example.com",
        "password": "masifansarisecret",
    },
    "adnanansari": {
        "username": "adnanansari",
        "full_name": "Adnan Ansari",
        "email": "pakaiverse@gmail.com",
        "password": "adnan123",
    },
    
}



@app.post("/login")
def login_request(data_from_user: Annotated [OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)]):
    
   
    # step 1 user Exits in Database ?
    
    username_in_db = fake_users_db.get(data_from_user.username)
    if username_in_db is None:
        raise HTTPException(status_code=400,detail="Incorrect Username")
    # step 2 Check Password else error
    if username_in_db["password"] != data_from_user.password:
        raise HTTPException(status_code=400,detail="Incorect Password")
    # step 3 generate token
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(subject=data_from_user.username, expires_delta=access_token_expires)
    print(data_from_user.username, data_from_user.password)
    return {"username": data_from_user.username, "access_token":access_token}
    
    
@app.get("/all-users")
def get_all_users():
    print(fake_users_db)
    return fake_users_db

@app.get("/new_route")
def get_access_token(username: str):
    """
    Understanding the access token
    -> Takes user_name as input and returns access token
    -> timedelta(minutes=1) is used to set the expiry time of the access token to 1 minute
    """
    
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(subject=username, expires_delta=access_token_expires)
    
    return {"access_token": access_token}



@app.get("/")
def read():
    return{"Hello" : "World"}

@app.get("/decode_token")
def decoding_token(access_token: str):
    """
    Understanding the access token decoding and validation
    """
    try:
        decoded_token_data = decode_access_token(access_token)
        return {"decoded_token": decoded_token_data}
    except JWTError as e:
        return {"error": str(e)}

