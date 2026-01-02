# models/forum.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from core.database import Base


class Forum(Base):
    __tablename__ = "forums"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    thematic = Column(String, nullable=False)  # Category/topic
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships with cascade delete
    moderators = relationship(
        "ForumModerator", 
        back_populates="forum", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    posts = relationship(
        "Post", 
        back_populates="forum", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class ForumModerator(Base):
    __tablename__ = "forum_moderators"
    
    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forums.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    forum = relationship("Forum", back_populates="moderators")
    user = relationship("User")


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forums.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_reported = Column(Boolean, default=False)
    report_reason = Column(Text, nullable=True)
    
    # Relationships with cascade delete
    forum = relationship("Forum", back_populates="posts")
    author = relationship("User")
    responses = relationship(
        "Response", 
        back_populates="post", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    likes = relationship(
        "PostLike", 
        back_populates="post", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_reported = Column(Boolean, default=False)
    report_reason = Column(Text, nullable=True)
    
    # Relationships with cascade delete
    post = relationship("Post", back_populates="responses")
    author = relationship("User")
    likes = relationship(
        "ResponseLike", 
        back_populates="response", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class PostLike(Base):
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="likes")
    user = relationship("User")


class ResponseLike(Base):
    __tablename__ = "response_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    response = relationship("Response", back_populates="likes")
    user = relationship("User")
