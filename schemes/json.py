from typing import List, Optional
from pydantic import BaseModel

class http_json(BaseModel):
    detail: str
    status_code: int
    data: Optional[List] = None
    
    