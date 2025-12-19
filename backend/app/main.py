from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi import APIRouter #type: ignore
from .routers import predict, latest_data, history, news
from app.middleware.logging_middleware import logging_middleware
from app.middleware.error_middleware import error_middleware
from app.core.logger import logger


app = FastAPI(
    title="Stock Predictor API",
    version="1.0.0"
)

origins = [
    "*",  # Change to frontend domain later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(history.router, tags=["History"])
api_v1.include_router(latest_data.router, tags=["Latest Data"])
api_v1.include_router(news.router, tags=["News"])
api_v1.include_router(predict.router, tags=["Predictions"])

app.include_router(api_v1)
app.middleware("http")(logging_middleware)
app.middleware("http")(error_middleware)

logger.info("Starting Stock Predictor API...")

#uvicorn app.main:app --reload