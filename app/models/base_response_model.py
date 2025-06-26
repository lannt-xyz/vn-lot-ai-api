from typing import Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_camelcase import CamelModel

class BaseResponseModel(CamelModel):
    detail: Any = "Success"

    @staticmethod
    def ok() -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(BaseResponseModel()))

    @staticmethod
    def ok(data: CamelModel) -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(data))

    @staticmethod
    def no_content() -> JSONResponse:
        return JSONResponse(
            status_code=204,
            content=jsonable_encoder(BaseResponseModel(detail="No content"))
        )

