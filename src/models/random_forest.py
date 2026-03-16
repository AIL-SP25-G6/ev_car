"""
Random Forest Regression — stub for teammate implementation.

Uses unscaled features + raw VND target.
GridSearchCV tunes n_estimators, max_depth, min_samples_split, min_samples_leaf.

TODO: Implement full training pipeline. The BaseModel.run() method handles
      data loading, training, evaluation, and plot generation automatically.
      Just ensure create_model() returns the correct estimator.
"""

from sklearn.ensemble import RandomForestRegressor

from .base_model import BaseModel
from .config import register_model, RANDOM_STATE


@register_model("random_forest")
class RandomForestModel(BaseModel):
    name = "random_forest"
    model_type = "unscaled_raw"

    def create_model(self):
        return RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)

    # TODO: Override train() if custom logic is needed (e.g., feature selection).
    # TODO: Override get_param_grid() to adjust the search space if needed.
    # The default grid is in config.py under PARAM_GRIDS["random_forest"].
