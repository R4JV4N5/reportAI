from pydantic import BaseModel

class ReportRequest(BaseModel):
    start_date: str
    end_date: str


class ReportResponse(BaseModel):
    message: str
    status: int
    data: dict
