# src/metrics_drift.py
import numpy as np
from scipy.stats import ks_2samp
from sklearn.metrics import mean_squared_error


def detect_data_drift(reference_data, current_data, threshold=0.1):
    """
    Detects data drift between reference and current datasets using the Kolmogorov-Smirnov test.
    Higher threshold values make drift detection less sensitive.
    overall_drift_score = mean of all KS statistics across columns, representing the overall drift magnitude.
    """
    drift_scores = {}
    for column in reference_data.columns:
        ks_statistic, p_value = ks_2samp(reference_data[column], current_data[column])
        drift_scores[column] = ks_statistic

    overall_drift_score = np.mean(list(drift_scores.values()))
    is_drift = overall_drift_score > threshold

    return is_drift, drift_scores, overall_drift_score
    

def detect_concept_drift(
    model_pipeline, X_reference, y_reference, X_current, y_current, threshold=0.1):
    """
    Detects concept drift by comparing model performance change between reference and current datasets
    using Mean Squared Error (MSE)
    
    relative_performance_decrease : performance as a ratio (MSE_current - MSE_reference) / MSE_reference.
    Positive values indicate performance degradation, negative values indicate improvement.
    """
    
    y_pred_reference = model_pipeline.predict(X_reference)
    y_pred_current = model_pipeline.predict(X_current)

    mse_reference = mean_squared_error(y_reference, y_pred_reference)
    mse_current = mean_squared_error(y_current, y_pred_current)

    relative_performance_decrease = (mse_current - mse_reference) / mse_reference
    is_drift = relative_performance_decrease > threshold

    return is_drift, relative_performance_decrease
