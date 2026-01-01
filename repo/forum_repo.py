# repo/forum_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.forum import Forum, ForumModerator, Post, Response, PostLike, ResponseLike
from typing import List, Optional

# Forum operations
def create_forum(db: Session, name: str, description: Optional[str], thematic: str, moderator_ids: List[int]):
    if not moderator_ids:
        raise ValueError("At least one moderator is required")
    
    forum = Forum(name=name, description=description, thematic=thematic)
    db.add(forum)
    db.flush()
    
    # Add moderators
    for mod_id in moderator_ids:
        moderator = ForumModerator(forum_id=forum.id, user_id=mod_id)
        db.add(moderator)
    
    db.commit()
    db.refresh(forum)
    return forum

def get_forum_by_id(db: Session, forum_id: int):
    return db.query(Forum).filter(Forum.id == forum_id, Forum.is_active == True).first()

def get_all_forums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Forum).filter(Forum.is_active == True).offset(skip).limit(limit).all()

def get_forums_by_thematic(db: Session, thematic: str):
    return db.query(Forum).filter(Forum.thematic == thematic, Forum.is_active == True).all()

# Post operations
def create_post(db: Session, forum_id: int, author_id: int, title: str, content: str, is_anonymous: bool):
    post = Post(
        forum_id=forum_id,
        author_id=author_id,
        title=title,
        content=content,
        is_anonymous=is_anonymous
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts_by_forum(db: Session, forum_id: int, skip: int = 0, limit: int = 50):
    return db.query(Post).filter(Post.forum_id == forum_id).offset(skip).limit(limit).all()

def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    return db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()

def update_post(db: Session, post_id: int, title: Optional[str] = None, content: Optional[str] = None):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

def report_post(db: Session, post_id: int, reason: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    
    post.is_reported = True
    post.report_reason = reason
    db.commit()
    db.refresh(post)
    return post

# Response operations
def create_response(db: Session, post_id: int, author_id: int, content: str, is_anonymous: bool):
    response = Response(
        post_id=post_id,
        author_id=author_id,
        content=content,
        is_anonymous=is_anonymous
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

def get_response_by_id(db: Session, response_id: int):
    return db.query(Response).filter(Response.id == response_id).first()

def get_responses_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Response).filter(Response.post_id == post_id).offset(skip).limit(limit).all()

def update_response(db: Session, response_id: int, content: str):
    response = db.query(Response).filter(Response.id == response_id).first()
    if not response:
        return None
    
    response.content = content
    db.commit()
    db.refresh(response)
    return response

def delete_response(db: Session, response_id: int):
    response = db.query(Response).filter(Response.id == response_id).first()
    if response:
        db.delete(response)
        db.commit()
        return True
    return False

def report_response(db: Session, response_id: int, reason: str):
    response = db.query(Response).filter(Response.id == response_id).first()
    if not response:
        return None
    
    response.is_reported = True
    response.report_reason = reason
    db.commit()
    db.refresh(response)
    return response

# Like operations
def toggle_post_like(db: Session, post_id: int, user_id: int):
    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == user_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return False  # Unlike
    else:
        like = PostLike(post_id=post_id, user_id=user_id)
        db.add(like)
        db.commit()
        return True  # Like

def toggle_response_like(db: Session, response_id: int, user_id: int):
    existing_like = db.query(ResponseLike).filter(
        ResponseLike.response_id == response_id,
        ResponseLike.user_id == user_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return False  # Unlike
    else:
        like = ResponseLike(response_id=response_id, user_id=user_id)
        db.add(like)
        db.commit()
        return True  # Like

def get_post_like_count(db: Session, post_id: int):
    return db.query(func.count(PostLike.id)).filter(PostLike.post_id == post_id).scalar()

def get_response_like_count(db: Session, response_id: int):
    return db.query(func.count(ResponseLike.id)).filter(ResponseLike.response_id == response_id).scalar()

def get_response_count_for_post(db: Session, post_id: int):
    return db.query(func.count(Response.id)).filter(Response.post_id == post_id).scalar()