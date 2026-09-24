from pydantic import BaseModel, Field


class FraudRequest(BaseModel):

    amount: float = Field(gt=0)

    merchant: str

    hour: int = Field(
        ge=0,
        le=23,
    )

    transaction_count_24h: int = Field(
        ge=0
    )

    avg_amount_30d: float = Field(
        ge=0
    )


class FraudResponse(BaseModel):

    fraud_probability: float

    decision: str


class CreditRequest(BaseModel):

    income: float = Field(gt=0)

    age: int = Field(
        ge=18,
        le=100,
    )

    loan_amount: float = Field(gt=0)

    debt_to_income: float = Field(
        ge=0
    )


class CreditResponse(BaseModel):

    risk_probability: float

    risk_level: str


class ChurnRequest(BaseModel):

    tenure_months: int = Field(
        ge=0
    )

    monthly_spend: float = Field(
        ge=0
    )

    support_tickets: int = Field(
        ge=0
    )

    login_count: int = Field(
        ge=0
    )


class ChurnResponse(BaseModel):

    churn_probability: float

    risk_level: str


class RecommendationResponse(BaseModel):

    customer_id: str

    products: list[str]