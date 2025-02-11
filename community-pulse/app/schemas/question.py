from pydantic import BaseModel
from typing import Optional

# ---------------------- CATEGORY SCHEMAS ----------------------

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


# ---------------------- QUESTION SCHEMAS ----------------------
class QuestionResponse(BaseModel):
    id: int
    text: str
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    text: str
    category_id: Optional[int] = None


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    category_id: Optional[int] = None


