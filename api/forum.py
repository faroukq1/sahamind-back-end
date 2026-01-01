# api/forum.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from repo import forum_repo
from schemas.forum import (
    ForumCreate, ForumResponse,
    PostCreate, PostUpdate, PostResponse,
    ResponseCreate, ResponseUpdate, ResponseResponse,
    ReportContent
)

router = APIRouter(prefix="/forums", tags=["forums"])

# =====================================================
# POSTS
# =====================================================

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    """
    Create a post.
    user_id is provided in the request body (NO auth dependency).
    """

    post = forum_repo.create_post(
        db=db,
        forum_id=data.forum_id,
        author_id=data.user_id,
        title=data.title,
        content=data.content,
        is_anonymous=data.is_anonymous
    )

    return {
        "id": post.id,
        "forum_id": post.forum_id,
        "author_id": post.author_id,
        "title": post.title,
        "content": post.content,
        "is_anonymous": post.is_anonymous,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "like_count": 0,
        "response_count": 0
    }


@router.get("/{forum_id}/posts", response_model=List[PostResponse])
def get_posts_for_forum(forum_id: int, db: Session = Depends(get_db)):
    posts = forum_repo.get_posts_by_forum(db, forum_id)

    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "forum_id": post.forum_id,
            "author_id": post.author_id,
            "title": post.title,
            "content": post.content,
            "is_anonymous": post.is_anonymous,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "like_count": forum_repo.get_post_like_count(db, post.id),
            "response_count": forum_repo.get_response_count_for_post(db, post.id)
        })

    return result


@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    user_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db)
):
    post = forum_repo.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_post = forum_repo.update_post(
        db,
        post_id,
        data.title,
        data.content
    )

    return {
        "id": updated_post.id,
        "forum_id": updated_post.forum_id,
        "author_id": updated_post.author_id,
        "title": updated_post.title,
        "content": updated_post.content,
        "is_anonymous": updated_post.is_anonymous,
        "created_at": updated_post.created_at,
        "updated_at": updated_post.updated_at,
        "like_count": forum_repo.get_post_like_count(db, post_id),
        "response_count": forum_repo.get_response_count_for_post(db, post_id)
    }


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post = forum_repo.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    forum_repo.delete_post(db, post_id)


# =====================================================
# RESPONSES
# =====================================================

@router.post("/responses", response_model=ResponseResponse, status_code=status.HTTP_201_CREATED)
def create_response(data: ResponseCreate, db: Session = Depends(get_db)):
    response = forum_repo.create_response(
        db=db,
        post_id=data.post_id,
        author_id=data.user_id,
        content=data.content,
        is_anonymous=data.is_anonymous
    )

    return {
        "id": response.id,
        "post_id": response.post_id,
        "author_id": response.author_id,
        "content": response.content,
        "is_anonymous": response.is_anonymous,
        "created_at": response.created_at,
        "updated_at": response.updated_at,
        "like_count": 0
    }


@router.get("/posts/{post_id}/responses", response_model=List[ResponseResponse])
def get_responses(post_id: int, db: Session = Depends(get_db)):
    responses = forum_repo.get_responses_by_post(db, post_id)

    return [
        {
            "id": r.id,
            "post_id": r.post_id,
            "author_id": r.author_id,
            "content": r.content,
            "is_anonymous": r.is_anonymous,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "like_count": forum_repo.get_response_like_count(db, r.id)
        }
        for r in responses
    ]


@router.put("/responses/{response_id}", response_model=ResponseResponse)
def update_response(
    response_id: int,
    user_id: int,
    data: ResponseUpdate,
    db: Session = Depends(get_db)
):
    response = forum_repo.get_response_by_id(db, response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")

    if response.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated = forum_repo.update_response(db, response_id, data.content)

    return {
        "id": updated.id,
        "post_id": updated.post_id,
        "author_id": updated.author_id,
        "content": updated.content,
        "is_anonymous": updated.is_anonymous,
        "created_at": updated.created_at,
        "updated_at": updated.updated_at,
        "like_count": forum_repo.get_response_like_count(db, response_id)
    }


@router.delete("/responses/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_response(response_id: int, user_id: int, db: Session = Depends(get_db)):
    response = forum_repo.get_response_by_id(db, response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")

    if response.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    forum_repo.delete_response(db, response_id)


# =====================================================
# REPORTING
# =====================================================

@router.post("/posts/{post_id}/report")
def report_post(post_id: int, data: ReportContent, db: Session = Depends(get_db)):
    post = forum_repo.report_post(db, post_id, data.reason)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post reported successfully"}


@router.post("/responses/{response_id}/report")
def report_response(response_id: int, data: ReportContent, db: Session = Depends(get_db)):
    response = forum_repo.report_response(db, response_id, data.reason)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return {"message": "Response reported successfully"}
