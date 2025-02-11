from pydantic import BaseModel, Field


# ---------------------- RESPONSE SCHEMAS ----------------------
class ResponseCreate(BaseModel):
    question_id: int = Field(..., description="ID вопроса")
    is_agree: bool = Field(..., description="Согласие или несогласие с вопросом")


class StatisticResponse(BaseModel):
    question_id: int
    agree_count: int = Field(..., ge=0, description="Количество согласных ответов")
    disagree_count: int = Field(..., ge=0, description="Количество несогласных ответов")