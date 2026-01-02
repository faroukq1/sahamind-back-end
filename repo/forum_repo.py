# repo/forum_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.forum import Forum, ForumModerator, Post, Response, PostLike, ResponseLike
from typing import List, Optional


# =====================================================
# FORUM OPERATIONS
# =====================================================

def get_all_forums(db: Session, skip: int = 0, limit: int = 100) -> List[Forum]:
    """Get all active forums"""
    return db.query(Forum).filter(Forum.is_active == True).offset(skip).limit(limit).all()


def get_forum_by_id(db: Session, forum_id: int) -> Optional[Forum]:
    """Get a single forum by ID"""
    return db.query(Forum).filter(Forum.id == forum_id, Forum.is_active == True).first()


def get_forums_by_thematic(db: Session, thematic: str) -> List[Forum]:
    """Get forums by thematic category"""
    return db.query(Forum).filter(Forum.thematic == thematic, Forum.is_active == True).all()


def create_forum(db: Session, name: str, description: Optional[str], thematic: str, moderator_ids: List[int]) -> Forum:
    """Create a new forum with moderators"""
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


def get_moderator_count(db: Session, forum_id: int) -> int:
    """Get count of moderators for a forum"""
    return db.query(ForumModerator).filter(ForumModerator.forum_id == forum_id).count()


def get_post_count_for_forum(db: Session, forum_id: int) -> int:
    """Get count of posts in a forum"""
    return db.query(Post).filter(Post.forum_id == forum_id).count()


# =====================================================
# POST OPERATIONS
# =====================================================

def create_post(db: Session, forum_id: int, author_id: int, title: str, content: str, is_anonymous: bool) -> Post:
    """Create a new post"""
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


def get_post_by_id(db: Session, post_id: int) -> Optional[Post]:
    """Get a single post by ID"""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts_by_forum(db: Session, forum_id: int, skip: int = 0, limit: int = 50) -> List[Post]:
    """Get all posts for a specific forum"""
    return db.query(Post).filter(Post.forum_id == forum_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[Post]:
    """Get all posts by a specific user"""
    return db.query(Post).filter(Post.author_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def update_post(db: Session, post_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Post]:
    """Update a post"""
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


def delete_post(db: Session, post_id: int) -> bool:
    """Delete a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False


def report_post(db: Session, post_id: int, reason: str) -> Optional[Post]:
    """Report a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    
    post.is_reported = True
    post.report_reason = reason
    db.commit()
    db.refresh(post)
    return post


def get_post_like_count(db: Session, post_id: int) -> int:
    """Get like count for a post"""
    return db.query(func.count(PostLike.id)).filter(PostLike.post_id == post_id).scalar() or 0


def get_response_count_for_post(db: Session, post_id: int) -> int:
    """Get count of responses for a post"""
    return db.query(func.count(Response.id)).filter(Response.post_id == post_id).scalar() or 0


# =====================================================
# RESPONSE OPERATIONS
# =====================================================

def create_response(db: Session, post_id: int, author_id: int, content: str, is_anonymous: bool) -> Response:
    """Create a new response"""
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


def get_response_by_id(db: Session, response_id: int) -> Optional[Response]:
    """Get a single response by ID"""
    return db.query(Response).filter(Response.id == response_id).first()


def get_responses_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Response]:
    """Get all responses for a specific post"""
    return db.query(Response).filter(Response.post_id == post_id).order_by(Response.created_at.asc()).offset(skip).limit(limit).all()


def update_response(db: Session, response_id: int, content: str) -> Optional[Response]:
    """Update a response"""
    response = db.query(Response).filter(Response.id == response_id).first()
    if not response:
        return None
    
    response.content = content
    db.commit()
    db.refresh(response)
    return response


def delete_response(db: Session, response_id: int) -> bool:
    """Delete a response"""
    response = db.query(Response).filter(Response.id == response_id).first()
    if response:
        db.delete(response)
        db.commit()
        return True
    return False


def report_response(db: Session, response_id: int, reason: str) -> Optional[Response]:
    """Report a response"""
    response = db.query(Response).filter(Response.id == response_id).first()
    if not response:
        return None
    
    response.is_reported = True
    response.report_reason = reason
    db.commit()
    db.refresh(response)
    return response


def get_response_like_count(db: Session, response_id: int) -> int:
    """Get like count for a response"""
    return db.query(func.count(ResponseLike.id)).filter(ResponseLike.response_id == response_id).scalar() or 0


# =====================================================
# LIKE OPERATIONS
# =====================================================

def toggle_post_like(db: Session, post_id: int, user_id: int) -> bool:
    """Toggle like on a post. Returns True if liked, False if unliked"""
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


def toggle_response_like(db: Session, response_id: int, user_id: int) -> bool:
    """Toggle like on a response. Returns True if liked, False if unliked"""
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