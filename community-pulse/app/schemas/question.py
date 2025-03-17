from pydantic import BaseModel
from typing import List, Optional

# ---------------------- CATEGORY SCHEMAS ----------------------

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


# ---------------------- QUESTION SCHEMAS ----------------------

class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    category_ids: List[int]  # При создании передаем ID категорий


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    category_ids: Optional[List[int]] = None  # При обновлении можно обновить категории


class QuestionResponse(BaseModel):
    id: int
    text: str
    categories: List[CategoryResponse]  # Возвращаем категории

    class Config:
        from_attributes = True


