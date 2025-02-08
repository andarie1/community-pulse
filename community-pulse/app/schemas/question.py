from pydantic import BaseModel

class QuestionResponse(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True
        from_attributes = True

