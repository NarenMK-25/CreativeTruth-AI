import pytest
import pandas as pd
from engine import calculate_metrics, detect_illusions, evaluate_evidence

def test_calculate_metrics_zero_division():
    df = pd.DataFrame({
        'Impressions': [1000, 0],
        'Clicks': [50, 0],
        'Conversions': [5, 0],
        'Spend': [10.0, 0.0],
        'Revenue': [50.0, 0.0]
    })
    result = calculate_metrics(df)
    assert result['CTR'].iloc[1] == 0
    assert result['CVR'].iloc[1] == 0
    assert result['CPA'].iloc[1] == 0
    assert result['ROAS'].iloc[1] == 0
    assert result['CTR'].iloc[0] == 5.0
    
def test_illusion_detector():
    df = pd.DataFrame({
        'Ad ID': ['A', 'B', 'C', 'D'],
        'CTR': [10, 1, 5, 12],
        'CVR': [0.1, 10, 5, 0.05]
    })
    res = detect_illusions(df)
    assert 'A' in res['Ad ID'].values or 'D' in res['Ad ID'].values

def test_evidence_debt_insufficient_data():
    g1 = pd.DataFrame({'CTR': [1, 2]})
    g2 = pd.DataFrame({'CTR': [3, 4]})
    status, msg, n_h, n_l, effect, pval = evaluate_evidence(g1, g2)
    assert status == "INSUFFICIENT DATA"
