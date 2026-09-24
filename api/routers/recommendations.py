from fastapi import APIRouter

from api.schemas import (
    RecommendationResponse,
)


router = APIRouter()


@router.get(
    "/{customer_id}",
    response_model=RecommendationResponse,
)
def recommendations(
    customer_id: str,
):

    products = [
        "Premium Credit Card",
        "Personal Loan",
        "Investment Account",
    ]

    return RecommendationResponse(
        customer_id=customer_id,
        products=products,
    )