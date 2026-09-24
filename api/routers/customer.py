from fastapi import APIRouter


router = APIRouter()


@router.get("/{customer_id}")
def get_customer(
    customer_id: str,
):

    return {
        "customer_id": customer_id,
        "status": "ACTIVE",
        "profile": {
            "segment": "PREMIUM",
            "products": [
                "CURRENT_ACCOUNT",
                "CREDIT_CARD",
            ],
        },
    }