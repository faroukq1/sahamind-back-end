# schemas/forum.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


# Forum Schemas
class ForumCreate(BaseModel):
    name: str
    description: Optional[str] = None
    thematic: str
    moderator_ids: List[int]  # At least one moderator required

class ForumResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    thematic: str
    created_at: datetime
    is_active: bool
    moderator_count: int
    post_count: int
    
    class Config:
        from_attributes = True

# Post Schemas
class PostCreate(BaseModel):
    forum_id: int
    user_id: int
    title: str
    content: str
    is_anonymous: bool = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    

class PostResponse(BaseModel):
    id: int
    forum_id: int
    author_id: int
    author_name: str  # Add this field
    title: str
    content: str
    is_anonymous: bool
    created_at: datetime
    updated_at: datetime
    like_count: int
    response_count: int

    class Config:
        from_attributes = True


# Response Schemas
class ResponseCreate(BaseModel):
    post_id: int
    user_id: int
    content: str
    is_anonymous: bool = True

class ResponseUpdate(BaseModel):
    content: Optional[str] = None

class ResponseResponse(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    is_anonymous: bool
    created_at: datetime
    updated_at: datetime
    like_count: int
    
    class Config:
        from_attributes = True

# Report Schema
class ReportContent(BaseModel):
    reason: str




class PostOut(BaseModel):
    id: int
    forum_id: int
    author_id: int
    title: str
    content: str
    is_anonymous: bool
    created_at: datetime

    like_count: int
    response_count: int

    class Config:
        from_attributes = True
