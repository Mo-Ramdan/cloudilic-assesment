from pydantic import BaseModel, HttpUrl


class UrlRequest(BaseModel):
    url: HttpUrl

class SummarizeRequest(BaseModel):
    data: str
    
    
