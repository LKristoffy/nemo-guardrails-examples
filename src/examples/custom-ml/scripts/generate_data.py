import numpy as np
import pandas as pd

def create_synthetic_dataset(n_samples=1000, bias_level=0.3):
    """
    Create a synthetic dataset with a protected attribute and some bias.

    Args:
        n_samples: Number of samples to generate
        bias_level: Level of bias to introduce (0 to 1)

    Returns:
        Pandas DataFrame with features, protected attribute, and target
    """
    # Generate protected attribute (e.g., gender)
    protected = np.random.choice([0, 1], size=n_samples)

    # Generate features
    X1 = np.random.normal(0, 1, n_samples)
    X2 = np.random.normal(0, 1, n_samples)

    # Generate target with bias
    # The bias is introduced by making the weight of X1 different based on the protected attribute
    y = (0.5 * X1 + 1.0 * X2 > 0).astype(int)

    # Introduce bias: flip some labels for the disadvantaged group
    disadvantaged_mask = protected == 0
    non_disadvantaged_mask = protected == 1
    flip_mask = np.random.random(n_samples) < bias_level
    flip_mask_2 = np.random.random(n_samples) < (1 - bias_level)
    y[disadvantaged_mask & flip_mask & (y == 1)] = 0
    #y[non_disadvantaged_mask & flip_mask_2 & (y == 0)] = 1

    # Create DataFrame
    df = pd.DataFrame({"X1": X1, "X2": X2, "protected_attribute": protected, "target": y})

    return df