from fastapi import FastAPI

from api.routers import (
    fraud,
    credit,
    churn,
    customer,
    recommendations,
)


app = FastAPI(
    title="BankCore Intelligence API",
    version="1.0.0",
    description=(
        "Azure MLOps banking intelligence platform"
    ),
)


app.include_router(
    fraud.router,
    prefix="/api/v1/fraud",
    tags=["Fraud"],
)

app.include_router(
    credit.router,
    prefix="/api/v1/credit",
    tags=["Credit"],
)

app.include_router(
    churn.router,
    prefix="/api/v1/churn",
    tags=["Churn"],
)

app.include_router(
    customer.router,
    prefix="/api/v1/customers",
    tags=["Customers"],
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "bankcore-api",
    }


@app.get("/model/info")
def model_info():

    return {
        "model": "bankcore",
        "version": "1.0",
        "environment": "dev",
    }