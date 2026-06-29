from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base,engine

from app.routes import auth,products,cart,orders,payments
from app.utils.logger import get_logger


# logger

logger=get_logger(__name__)


# create tables

Base.metadata.create_all(bind=engine)


# fastapi app

app=FastAPI(title="E-Commerce Order Management System",version="1.0.0",description="End-to-End Backend Application using FastAPI")


# cors

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])


# startup event

@app.on_event("startup")
def startup():
    logger.info("application started successfully")


# shutdown event

@app.on_event("shutdown")
def shutdown():
    logger.info("application stopped")


# root api

@app.get("/")
def root():
    logger.info("root endpoint accessed")
    return {"message":"welcome to e-commerce order management system"}


# routers

app.include_router(auth.router,prefix="/api/v1")
app.include_router(products.router,prefix="/api/v1")
app.include_router(cart.router,prefix="/api/v1")
app.include_router(orders.router,prefix="/api/v1")
app.include_router(payments.router,prefix="/api/v1")