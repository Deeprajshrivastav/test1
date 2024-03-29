from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # for default value
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes = True 
        
        
class CreatePost(PostBase):
    pass
        
class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool = True  # for default value
    
class Post(PostBase):  
    
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    class ConfigDict:
        from_attributes = True 

class PostOut(BaseModel):
    Post: Post
    Votes: int
    class ConfigDict:
        from_attributes = True 



class UserCreate(BaseModel):
    email: EmailStr
    password: str    
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None    
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
    
    
