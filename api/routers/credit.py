from pathlib import Path

import joblib
import pandas as pd

from fastapi import APIRouter

from api.schemas import (
    CreditRequest,
    CreditResponse,
)


router = APIRouter()


MODEL_PATH = Path(
    "models/credit/model.joblib"
)


@router.post(
    "/predict",
    response_model=CreditResponse,
)
def predict(
    request: CreditRequest,
):

    if not MODEL_PATH.exists():

        probability = 0.0

    else:

        bundle = joblib.load(
            MODEL_PATH
        )

        row = pd.DataFrame(
            [
                {
                    "income": request.income,
                    "age": request.age,
                    "loan_amount":
                        request.loan_amount,
                    "debt_to_income":
                        request.debt_to_income,
                }
            ]
        )

        probability = float(
            bundle["model"]
            .predict_proba(row)[0][1]
        )

    if probability >= 0.70:
        risk = "HIGH"

    elif probability >= 0.40:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return CreditResponse(
        risk_probability=probability,
        risk_level=risk,
    )