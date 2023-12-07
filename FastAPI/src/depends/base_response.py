from typing import Any
import pydantic as _pd


class BaseResponseModel(_pd.BaseModel):
    data: Any = {}
    meta: dict = {}
    success: bool = True
    code: int = 200
    message: str = 'Success'
