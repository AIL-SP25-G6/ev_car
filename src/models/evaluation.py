"""
Evaluation metrics for regression models.

All metrics are computed in original VND scale.
"""

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from .config import RANDOM_STATE


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_features: int,
) -> dict:
    """
    Compute a comprehensive set of regression metrics.

    Parameters
    ----------
    y_true : array-like — ground truth (VND)
    y_pred : array-like — predictions (VND)
    n_features : int — number of features (for Adjusted R2)

    Returns
    -------
    dict with keys: mse, rmse, mae, r2, adj_r2, mape
    """
    n = len(y_true)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    # Adjusted R2
    if n > n_features + 1:
        adj_r2 = 1 - (1 - r2) * (n - 1) / (n - n_features - 1)
    else:
        adj_r2 = r2

    # MAPE (guard against zero values)
    mask = y_true != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan

    return {
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "adj_r2": adj_r2,
        "mape": mape,
    }


def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_bootstrap: int = 1000,
    ci: float = 0.95,
) -> tuple[float, float]:
    """
    Bootstrap 95 % confidence interval on RMSE.

    Returns
    -------
    (lower_bound, upper_bound)
    """
    rng = np.random.RandomState(RANDOM_STATE)
    n = len(y_true)
    rmse_samples = np.empty(n_bootstrap)

    for i in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        rmse_samples[i] = np.sqrt(mean_squared_error(y_true[idx], y_pred[idx]))

    alpha = (1 - ci) / 2
    lower = np.percentile(rmse_samples, alpha * 100)
    upper = np.percentile(rmse_samples, (1 - alpha) * 100)
    return float(lower), float(upper)
