"""
Dataset splitting utilities for MediaForge Vision.

Creates stratified train / validation / test splits.
"""

from __future__ import annotations

import pandas as pd

from sklearn.model_selection import train_test_split


def split_dataframe(
    dataframe: pd.DataFrame,
    *,
    train_size: float = 0.80,
    validation_size: float = 0.10,
    test_size: float = 0.10,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split a dataframe into train, validation and test sets.

    Splitting is stratified using the label column whenever
    possible.
    """

    if abs(train_size + validation_size + test_size - 1.0) > 1e-6:
        raise ValueError(
            "train_size + validation_size + test_size must equal 1."
        )

    dataframe = dataframe.sample(
        frac=1.0,
        random_state=random_state,
    ).reset_index(drop=True)

    stratify = None

    if "label" in dataframe.columns:
        stratify = dataframe["label"]

    train_df, remaining_df = train_test_split(
        dataframe,
        train_size=train_size,
        random_state=random_state,
        stratify=stratify,
    )

    remaining_stratify = None

    if stratify is not None:
        remaining_stratify = remaining_df["label"]

    validation_fraction = validation_size / (
        validation_size + test_size
    )

    val_df, test_df = train_test_split(
        remaining_df,
        train_size=validation_fraction,
        random_state=random_state,
        stratify=remaining_stratify,
    )

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    train_df["split"] = "train"
    val_df["split"] = "validation"
    test_df["split"] = "test"

    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    return (
        train_df,
        val_df,
        test_df,
    )