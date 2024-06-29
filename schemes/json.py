from typing import List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class http_json(BaseModel):
    detail: str
    status_code: int
    data: Optional[dict] = None
    
    