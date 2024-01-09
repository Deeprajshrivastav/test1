from .. import schemas, models, utils, oath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter


router = APIRouter(
    
    prefix='/vote',
    tags=['vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def post_vote(vote: schemas.Vote, db: Session=Depends(get_db), current_user:int=Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    vote_query = db.query(models.Votes).filter(vote.post_id == models.Votes.post_id, current_user.id==models.Votes.user_id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} already vote on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)    
        db.add(new_vote)
        db.commit()
        return {"message": "Vote Created"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Vote deleted successfully'}
    
@router.get('/my')
def get_my_votes(db: Session=Depends(get_db), current_user:int=Depends(oath2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id)
    found_vote = vote_query.all()
    return found_vote

@router.get('/{post_id}', status_code=status.HTTP_200_OK)
def get_post_vote(post_id: int, db:Session=Depends(get_db), current_user:int=Depends(oath2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == post_id)
    vote_data = vote_query.all()
    for i in vote_data:
        print(i.user_id)
    pass

@router.get('/me/{post_id}')
def my_vote(post_id: int, db: Session=Depends(get_db), current_user:int=Depends(oath2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == post_id and current_user.id == models.votes.user_id)
    found_vote = vote_query.first()
    if found_vote:
        return {"voted": True}
    return {"voted": False}

