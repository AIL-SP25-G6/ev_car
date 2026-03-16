"""
XGBoost Regression — stub for teammate implementation.

Uses unscaled features + raw VND target.
GridSearchCV tunes n_estimators, max_depth, learning_rate, subsample, colsample_bytree.

TODO: Implement full training pipeline. The BaseModel.run() method handles
      data loading, training, evaluation, and plot generation automatically.
      Just ensure create_model() returns the correct estimator.
"""

from xgboost import XGBRegressor

from .base_model import BaseModel
from .config import register_model, RANDOM_STATE


@register_model("xgboost")
class XGBoostModel(BaseModel):
    name = "xgboost"
    model_type = "unscaled_raw"

    def create_model(self):
        return XGBRegressor(
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbosity=0,
        )

    # TODO: Override train() if custom logic is needed.
    # TODO: Consider early stopping with eval_set.
    # TODO: Override get_param_grid() to adjust the search space if needed.
    # The default grid is in config.py under PARAM_GRIDS["xgboost"].
