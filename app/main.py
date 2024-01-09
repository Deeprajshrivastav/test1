from fastapi import FastAPI, Depends, HTTPException

#from typing import Optional, List
#from psycopg2.extras import RealDictCursor
#from sqlalchemy.orm import Session
#from .utils import hashed_password
#import psycopg2
from .routers import post, user, auth, votes
from .config import Setting
from fastapi.middleware.cors import CORSMiddleware
#from .database import SessionLocal, engine, get_db
#from . import schemas, models, database
#models.Base.metadata.create_all(bind=engine) 

#models.Base.metadata.create_all(bind=engine)
"""

try:    
    conn = psycopg2.connect(
        host = 'localhost', 
        port = 5432,
        user = 'postgres',
        database = 'fastapi',
        password = '12345',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
except ConnectionError as connection_error:
    print('Connection Error: %s' % connection_error)
    
except Exception as error:
    print('Exception: %s' % error)
    
"""

from typing import Annotated


app =  FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def dummy(x: int):
    if x < 0:
        raise HTTPException(status_code=404, detail="Negative number")
    return {'msg': 'posstive integer'}
        

    
dep = Annotated[int, Depends(dummy)]

@app.get('/')
async def root():
    return {"message": "hello world"}


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(votes.router)
