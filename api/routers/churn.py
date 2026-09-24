from pathlib import Path

import joblib
import pandas as pd

from fastapi import APIRouter

from api.schemas import (
    ChurnRequest,
    ChurnResponse,
)


router = APIRouter()


MODEL_PATH = Path(
    "models/churn/model.joblib"
)


@router.post(
    "/predict",
    response_model=ChurnResponse,
)
def predict(
    request: ChurnRequest,
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
                    "tenure_months":
                        request.tenure_months,
                    "monthly_spend":
                        request.monthly_spend,
                    "support_tickets":
                        request.support_tickets,
                    "login_count":
                        request.login_count,
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

    return ChurnResponse(
        churn_probability=probability,
        risk_level=risk,
    )