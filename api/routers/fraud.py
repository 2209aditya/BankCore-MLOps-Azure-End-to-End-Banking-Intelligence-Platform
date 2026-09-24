from pathlib import Path

import joblib
import pandas as pd

from fastapi import APIRouter

from api.schemas import (
    FraudRequest,
    FraudResponse,
)


router = APIRouter()


MODEL_PATH = Path(
    "models/fraud/model.joblib"
)


def load_model():

    if not MODEL_PATH.exists():
        return None

    return joblib.load(
        MODEL_PATH
    )


@router.post(
    "/predict",
    response_model=FraudResponse,
)
def predict(
    request: FraudRequest,
):

    bundle = load_model()

    if bundle is None:

        probability = 0.0

    else:

        model = bundle["model"]

        columns = bundle["columns"]

        row = pd.DataFrame(
            [
                {
                    "amount": request.amount,
                    "merchant": request.merchant,
                    "hour": request.hour,
                    "transaction_count_24h":
                        request.transaction_count_24h,
                    "avg_amount_30d":
                        request.avg_amount_30d,
                }
            ]
        )

        row = pd.get_dummies(
            row,
            drop_first=True,
        )

        row = row.reindex(
            columns=columns,
            fill_value=0,
        )

        probability = float(
            model.predict_proba(row)[0][1]
        )

    decision = (
        "REVIEW"
        if probability >= 0.5
        else "ALLOW"
    )

    return FraudResponse(
        fraud_probability=probability,
        decision=decision,
    )