from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import  RequestValidationError
from fastapi.encoders import jsonable_encoder

from app import app
from app.logs import logger
from app.models.base_response_model import BaseResponseModel

@app.exception_handler(RequestValidationError)
# pylint: disable=unused-argument
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if not errors or len(errors) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(BaseResponseModel(detail="Invalid request data."))
        )

    # loop on each error, and get the needed information only
    error_details = []
    for error in errors:
        # for the `loc` key, we need to get the last item in the list
        error_details.append({
            "loc": error.get("loc")[len(error.get("loc")) - 1],
            "msg": error.get("msg"),
            "type": error.get("type"),
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(BaseResponseModel(detail=error_details)),
    )

@app.exception_handler(Exception)
# pylint: disable=unused-argument
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(BaseResponseModel(detail="System error occurred. Please try again later.")),
    )

@app.get("/health")
def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(BaseResponseModel(detail="Service is up and running.")),
    )
