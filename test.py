from pydantic import BaseModel
from typing import Optional

class Foo(BaseModel):
    count: int
    size: Optional[float] = None


obj = Foo(count=5)

print(obj)