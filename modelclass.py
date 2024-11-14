from pydantic import BaseModel

class ReportRequest(BaseModel):
    start_date: str
    end_date: str
    questions_list :list


class ReportResponse(BaseModel):
    message: str
    status: int
    data: str

class questionsResponse(BaseModel):
    message: str
    status: int
    data: list[str]