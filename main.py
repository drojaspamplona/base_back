import logging

import psycopg
import uvicorn
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from api import api_router
from config import settings
from domain.exceptions import DomainException
from domain.models.auth import TokeModel
from domain.services.auth import UserService
from infrastructure.commons.enums.error_message import ErrorMessageKey
from infrastructure.utils.locale import load_locales, translate_message

app = FastAPI(title=settings.project_name,
              openapi_url="/api/v1/openapi.json", docs_url=settings.docs_url)

app.add_middleware(CORSMiddleware,
                   allow_origins=[settings.allowed_origin],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=500)
app.include_router(api_router, prefix=settings.api_url)

load_locales()


@app.post("/token", response_model=TokeModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends()):
    return await service.login(form_data.username, form_data.password)


@app.get("/")
async def healt_check():
    return {"message": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(exc.errors())
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder(
                            {"message": translate_message(request, ErrorMessageKey.DEFAULT_ERROR)}))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logging.error(exc.detail)
    return JSONResponse(status_code=exc.status_code,
                        content=jsonable_encoder(
                            {"message": translate_message(request, ErrorMessageKey.DEFAULT_ERROR)}))


@app.exception_handler(DomainException)
async def http_exception_handler(request, exc: DomainException):
    logging.exception(exc.message)
    return JSONResponse(status_code=exc.code,
                        content=jsonable_encoder({"message": translate_message(request, exc.message)}))


@app.exception_handler(psycopg.Error)
async def http_exception_handler(request, exc: Exception):
    logging.exception(exc)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=jsonable_encoder(
                            {"message": translate_message(request, ErrorMessageKey.DEFAULT_ERROR)}))


# cd cli/
# python main.py -e organization -n Client

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
