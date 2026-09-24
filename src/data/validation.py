from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


TRANSACTION_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "timestamp",
    "merchant_category",
]


@dataclass
class ValidationResult:
    """Result returned by data validation."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rows: int = 0
    columns: int = 0

    def raise_if_invalid(self) -> None:
        """Raise an exception when validation fails."""

        if not self.valid:
            raise ValueError(
                "Data validation failed: "
                + "; ".join(self.errors)
            )


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> list[str]:
    """Return required columns that are missing."""

    return [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]


def validate_transactions(
    dataframe: pd.DataFrame,
) -> ValidationResult:
    """
    Validate transaction data used by fraud detection.

    Checks:
    - Required columns
    - Null customer IDs
    - Null transaction amounts
    - Negative amounts
    - Duplicate transaction IDs
    """

    errors: list[str] = []
    warnings: list[str] = []

    missing_columns = validate_required_columns(
        dataframe,
        TRANSACTION_COLUMNS,
    )

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )

    if "amount" in dataframe.columns:
        if dataframe["amount"].isna().any():
            errors.append(
                "amount contains null values"
            )

        if (dataframe["amount"] < 0).any():
            errors.append(
                "amount contains negative values"
            )

    if "customer_id" in dataframe.columns:
        if dataframe["customer_id"].isna().any():
            errors.append(
                "customer_id contains null values"
            )

    if "transaction_id" in dataframe.columns:
        duplicate_count = int(
            dataframe["transaction_id"].duplicated().sum()
        )

        if duplicate_count > 0:
            warnings.append(
                f"Found {duplicate_count} duplicate transaction IDs"
            )

    result = ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        rows=len(dataframe),
        columns=len(dataframe.columns),
    )

    logger.info(
        "Transaction validation completed: valid=%s rows=%d errors=%d warnings=%d",
        result.valid,
        result.rows,
        len(result.errors),
        len(result.warnings),
    )

    return result


def validate_no_nulls(
    dataframe: pd.DataFrame,
    columns: Optional[list[str]] = None,
) -> ValidationResult:
    """Validate that selected columns do not contain null values."""

    columns_to_check = columns or list(dataframe.columns)

    errors = []

    for column in columns_to_check:
        if column not in dataframe.columns:
            errors.append(
                f"Column not found: {column}"
            )
            continue

        null_count = int(
            dataframe[column].isna().sum()
        )

        if null_count > 0:
            errors.append(
                f"{column} contains {null_count} null values"
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        rows=len(dataframe),
        columns=len(dataframe.columns),
    )


def validate_numeric_range(
    dataframe: pd.DataFrame,
    column: str,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
) -> ValidationResult:
    """Validate numeric range for a dataframe column."""

    if column not in dataframe.columns:
        return ValidationResult(
            valid=False,
            errors=[f"Column not found: {column}"],
            rows=len(dataframe),
            columns=len(dataframe.columns),
        )

    errors = []

    series = dataframe[column]

    if not pd.api.types.is_numeric_dtype(series):
        errors.append(
            f"{column} must be numeric"
        )

    else:
        if minimum is not None:
            count = int(
                (series < minimum).sum()
            )

            if count:
                errors.append(
                    f"{column} has {count} values below {minimum}"
                )

        if maximum is not None:
            count = int(
                (series > maximum).sum()
            )

            if count:
                errors.append(
                    f"{column} has {count} values above {maximum}"
                )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        rows=len(dataframe),
        columns=len(dataframe.columns),
    )


def validate_dataframe(
    dataframe: pd.DataFrame,
    required_columns: Optional[list[str]] = None,
) -> ValidationResult:
    """
    Generic dataframe quality validation.

    This can be used before submitting data to an Azure ML training job.
    """

    errors: list[str] = []
    warnings: list[str] = []

    if dataframe.empty:
        errors.append(
            "DataFrame is empty"
        )

    if required_columns:
        missing = validate_required_columns(
            dataframe,
            required_columns,
        )

        if missing:
            errors.append(
                f"Missing required columns: {missing}"
            )

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    if duplicate_rows:
        warnings.append(
            f"Found {duplicate_rows} duplicate rows"
        )

    result = ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        rows=len(dataframe),
        columns=len(dataframe.columns),
    )

    logger.info(
        "Generic dataframe validation completed: valid=%s",
        result.valid,
    )

    return result