from jose import JWTError, jwt
from . import models
from fastapi import Depends, status, HTTPException
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database
from sqlalchemy.orm import Session
from . import config
import datetime

setting = config.Setting()
oath2_sechne = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expiry})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt



def verify_access_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data
    


def get_current_user(token: str = Depends(oath2_sechne), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail='Could not validate Credentials',
                                        headers={'WWW-Authenticate':'Bearer'})
    
    token =  verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
    