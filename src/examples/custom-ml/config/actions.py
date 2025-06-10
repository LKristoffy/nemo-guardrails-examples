from nemoguardrails.actions import action
import pandas as pd
from fairlearn.metrics import MetricFrame, selection_rate

@action(name="ValidateTabularDataAction")
def validate_tabular(csv_path: str,
                           sensitive: str, label: str):
    df = pd.read_csv(csv_path)


    # Fairness rail (Fairlearn)
    y_true = df[label]
    try:
        y_pred  = df['y_pred']
    except KeyError:
        raise KeyError("The DataFrame must contain a 'y_pred' column for predictions.")
    mf = MetricFrame(metrics={"sel_rate": selection_rate},
                     y_true=y_true, y_pred=y_pred,
                     sensitive_features=df[sensitive])
    dem_parity_gap = mf.difference(method="between_groups")
    fair_passed = abs(dem_parity_gap) < 0.05      # custom threshold

    return {
        "fair_passed": fair_passed,
        "dem_parity_gap": float(dem_parity_gap),
    }